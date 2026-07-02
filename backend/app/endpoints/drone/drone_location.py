# app/endpoints/drone/drone_location.py
import os
import json
import socket
import asyncio
import logging
from typing import Optional
from fastapi import APIRouter, Depends, status
import paho.mqtt.client as mqtt

from ...database import get_db
from ...models.emergency_responder import EmergencyResponder
from ...endpoints.mobile.user_info import get_current_user

router = APIRouter(prefix="/drone", tags=["Drone"])
logger = logging.getLogger(__name__)

current_drone_location = None

HIVEMQ_CLUSTER = os.getenv("HIVEMQ_CLUSTER")
HIVEMQ_USERNAME = os.getenv("HIVEMQ_USERNAME")
HIVEMQ_PASSWORD = os.getenv("HIVEMQ_PASSWORD")
HIVEMQ_TOPIC = os.getenv("HIVEMQ_TOPIC", "drone/telemetry")

mqtt_client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

def on_message(client, userdata, msg):
    global current_drone_location
    try:
        payload = json.loads(msg.payload.decode())
        current_drone_location = {
            "latitude": payload.get("latitude"),
            "longitude": payload.get("longitude"),
            "altitude": payload.get("altitude", 0.0),
            "speed": payload.get("speed", 0.0),
            "heading": payload.get("heading", 0.0),
            "status": "live"
        }
    except Exception as e:
        logger.error(f"Failed parsing broker telemetry payload: {e}")

if HIVEMQ_CLUSTER and HIVEMQ_USERNAME and HIVEMQ_PASSWORD:
    try:
        mqtt_client.username_pw_set(HIVEMQ_USERNAME, HIVEMQ_PASSWORD)
        mqtt_client.tls_set()
        mqtt_client.on_message = on_message
        mqtt_client.connect(HIVEMQ_CLUSTER, 8883)
        mqtt_client.subscribe(HIVEMQ_TOPIC)
        mqtt_client.loop_start()
        logger.info("FastAPI successfully connected to HiveMQ stream cluster.")
    except Exception as e:
        logger.error(f"MQTT init failure: {e}")

def listen_to_mission_planner():
    from pymavlink import mavutil
    global current_drone_location  # <--- Allow modifying the global variable
    
    logger.info("Opening local backend port on UDP 14550 for Mission Planner...")
    try:
        mav_conn = mavutil.mavlink_connection('udp:127.0.0.1:14550')
        
        while True:
            msg = mav_conn.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
            if msg:
                payload = {
                    "latitude": msg.lat / 1.0e7,
                    "longitude": msg.lon / 1.0e7,
                    "altitude": msg.alt / 1000.0,
                    "speed": msg.vx / 100.0,
                    "heading": msg.hdg / 100.0,
                    "status": "live"
                }
                
                # Direct local assignment so it updates IMMEDIATELY
                current_drone_location = payload
                
                # Still try to publish to the cloud if configured
                if HIVEMQ_CLUSTER:
                    try:
                        mqtt_client.publish(HIVEMQ_TOPIC, json.dumps(payload), qos=1)
                    except Exception as mqtt_err:
                        logger.error(f"Failed to publish to HiveMQ: {mqtt_err}")
                        
    except Exception as e:
        logger.error(f"Local Mission Planner UDP bridge error: {e}")

import threading
udp_thread = threading.Thread(target=listen_to_mission_planner, daemon=True)
udp_thread.start()

@router.get("/location", status_code=status.HTTP_200_OK)
async def get_drone_location(
    current_user: EmergencyResponder = Depends(get_current_user)
):
    if current_drone_location is None:
        return {
            "latitude": 14.5534,
            "longitude": 121.0471,
            "altitude": 120.5,
            "speed": 0.0,
            "status": "no_live_data"
        }
    return current_drone_location