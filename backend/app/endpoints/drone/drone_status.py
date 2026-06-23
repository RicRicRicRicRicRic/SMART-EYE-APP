# app/endpoints/drone/drone_status.py
"""
Endpoint and MQTT listener for real-time drone telemetry status.
"""

import os
import json
import logging
from fastapi import APIRouter, Depends, status
import paho.mqtt.client as mqtt

from ...database import get_db
from ...models.emergency_responder import EmergencyResponder
from ...endpoints.mobile.user_info import get_current_user

router = APIRouter(prefix="/drone", tags=["Drone"])
logger = logging.getLogger(__name__)

# Single persistent source of truth initialized as a dictionary to hold telemetry over time
local_drone_status = {
    "battery": None,
    "altitude": None,
    "speed": None,
    "status": "no_live_data"
}

# HiveMQ configuration variables
HIVEMQ_CLUSTER = os.getenv("HIVEMQ_CLUSTER")
HIVEMQ_USERNAME = os.getenv("HIVEMQ_USERNAME")
HIVEMQ_PASSWORD = os.getenv("HIVEMQ_PASSWORD")
HIVEMQ_TOPIC = os.getenv("HIVEMQ_TOPIC", "drone/telemetry")

def on_status_message(client, userdata, msg):
    global local_drone_status
    try:
        raw_payload = msg.payload.decode()
        payload = json.loads(raw_payload)
        
        # === ADD THESE DEBUG LINES ===
        logger.info(f"RAW MQTT Payload: {raw_payload[:1000]}...")  # Truncated if huge
        logger.info(f"Parsed Keys: {list(payload.keys())}")
        if isinstance(payload, dict):
            for k, v in list(payload.items())[:20]:  # Limit output
                if "batt" in k.lower() or "power" in k.lower() or "volt" in k.lower():
                    logger.info(f"Battery-related key found: {k} = {v}")
        # ============================
        
        # Mark status as live since we are actively receiving packets
        local_drone_status["status"] = "live"

        # 1. Update Altitude if present in this specific message packet
        if "altitude" in payload and payload["altitude"] is not None:
            local_drone_status["altitude"] = payload["altitude"]
        elif "alt" in payload and payload["alt"] is not None:
            local_drone_status["altitude"] = payload["alt"]

        # 2. Update Speed if present in this specific message packet
        if "speed" in payload and payload["speed"] is not None:
            local_drone_status["speed"] = payload["speed"]
        elif "groundspeed" in payload and payload["groundspeed"] is not None:
            local_drone_status["speed"] = payload["groundspeed"]

        # Improved Battery Extraction for Mission Planner MAVLink JSON
        battery_pct = None
        
        # 1. Direct top-level keys (most common)
        battery_keys = [
            "battery_remaining", "battery_percent", "battery_level", "battery",
            "remaining", "batt_remaining", "batt_pct", "soc", "charge"
        ]
        for key in battery_keys:
            if key in payload and payload[key] is not None:
                battery_pct = payload[key]
                logger.info(f"Found battery in top-level key: {key}")
                break

        # 2. Nested in common MAVLink message wrappers
        if battery_pct is None:
            for sub_key in ["battery_status", "BATTERY_STATUS", "sys_status", "SYS_STATUS", 
                          "vfr_hud", "VFR_HUD", "status", "power"]:
                if sub_key in payload and isinstance(payload[sub_key], dict):
                    inner = payload[sub_key]
                    for bkey in battery_keys + ["battery_remaining", "remaining", "voltage"]:
                        if bkey in inner and inner[bkey] is not None:
                            battery_pct = inner[bkey]
                            logger.info(f"Found battery in {sub_key}.{bkey}")
                            break
                    if battery_pct is not None:
                        break

        # 3. Deep search (brute force)
        if battery_pct is None:
            def find_battery(d, path=""):
                nonlocal battery_pct
                if battery_pct is not None:
                    return
                if isinstance(d, dict):
                    for k, v in d.items():
                        new_path = f"{path}.{k}" if path else k
                        if any(b in k.lower() for b in ["batt", "remain", "percent", "level", "soc", "charge"]):
                            if isinstance(v, (int, float)):
                                battery_pct = v
                                logger.info(f"Deep found battery at {new_path} = {v}")
                                return
                        elif isinstance(v, dict):
                            find_battery(v, new_path)
                        elif isinstance(v, list):
                            for i, item in enumerate(v):
                                find_battery(item, f"{new_path}[{i}]")
                elif isinstance(d, list):
                    for i, item in enumerate(d):
                        find_battery(item, f"{path}[{i}]")
            
            find_battery(payload)

        # 4. Final normalization
        if battery_pct is not None:
            try:
                val = float(battery_pct)
                # Convert 0-1 scale → 0-100 if needed
                if 0 < val <= 1.0:
                    val *= 100
                # Cap at reasonable values
                if val > 100:
                    val = 100
                local_drone_status["battery"] = int(val)
            except (ValueError, TypeError):
                logger.warning(f"Could not convert battery value: {battery_pct}")
                pass
        
        logger.info(f"Drone Status updated via HiveMQ: Battery={local_drone_status['battery']}, Alt={local_drone_status['altitude']}, Speed={local_drone_status['speed']}")
    except Exception as e:
        logger.error(f"Error parsing HiveMQ telemetry message: {e}")

# Initialize and connect MQTT client if credentials are present
if HIVEMQ_CLUSTER and HIVEMQ_USERNAME and HIVEMQ_PASSWORD:
    try:
        mqtt_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        mqtt_client.username_pw_set(HIVEMQ_USERNAME, HIVEMQ_PASSWORD)
        mqtt_client.tls_set()
        mqtt_client.on_message = on_status_message
        
        mqtt_client.connect(HIVEMQ_CLUSTER, 8883)
        mqtt_client.subscribe(HIVEMQ_TOPIC)
        mqtt_client.loop_start()
        logger.info(f"Connected to HiveMQ cluster: {HIVEMQ_CLUSTER}")
    except Exception as e:
        logger.error(f"Failed to connect to HiveMQ broker: {e}")
else:
    logger.warning("HiveMQ configuration missing in environment variables.")

@router.get("/status", status_code=status.HTTP_200_OK)
async def get_drone_status(
    current_user: EmergencyResponder = Depends(get_current_user)
):
    """
    Returns live drone telemetry status (Battery, Altitude, Speed).
    Returns 'no_live_data' status if no telemetry has been received.
    """
    if local_drone_status["status"] == "no_live_data":
        return {
            "battery": None,
            "altitude": None,
            "speed": None,
            "status": "no_live_data"
        }

    return {
        "battery": local_drone_status.get("battery"),
        "altitude": local_drone_status.get("altitude"),
        "speed": local_drone_status.get("speed"),
        "status": local_drone_status.get("status", "live")
    }