import requests
import time
from datetime import datetime
import json
import random

API_BASE_URL = "http://127.0.0.1:3000/api/drone/data"
API_KEY = "SUPER_SECRET_DRONE_KEY" 
DRONE_ID = "DRONE-ZETA-42"
INTERVAL_SECONDS = 5
ALERT_TYPES = ["FIRE_DETECTION", "MEDICAL_EMERGENCY", "VEHICLE_ACCIDENT", None, None] 

alert_id_counter = 5000 
latitude = 34.0522
longitude = -118.2437
battery = 100
altitude = 50.0

def generate_data(counter):
    global alert_id_counter, latitude, longitude, battery, altitude
    battery = max(10, battery - random.uniform(0.1, 0.5))
    latitude += random.uniform(-0.0001, 0.0001)
    longitude += random.uniform(-0.0001, 0.0001)
    emergency_type = random.choice(ALERT_TYPES)
    
    data = {
        "drone_id": DRONE_ID,
        "timestamp": datetime.utcnow().isoformat() + 'Z',
        "battery_percent": round(battery, 1),
        "altitude_meters": round(altitude + random.uniform(-5, 5), 2),
        "speed_mps": round(random.uniform(5, 25), 2)
    }

    if emergency_type:
        alert_id_counter += 1
        data.update({
            "emergency_type": emergency_type,
            "alert_id": alert_id_counter,
            "latitude": round(latitude, 6),
            "longitude": round(longitude, 6)
        })
    
    return data

def send_data(data):
    headers = {
        "Content-Type": "application/json",
        "X-Drone-API-Key": API_KEY
    }
    
    try:
        response = requests.post(API_BASE_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status() 
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Success: Status {response.status_code}. Message: {response.json().get('message')}")
        
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error sending data: {e}")
        if response is not None and response.text:
            print(f"Server response: {response.text}")

def run_simulator():
    print(f"Starting Drone Simulator for {DRONE_ID}. Sending data every {INTERVAL_SECONDS} seconds.")
    print("Press Ctrl+C to stop.")
    
    counter = 0
    while True:
        try:
            data = generate_data(counter)
            print(f"\n--- Sending Data (Alert: {'Yes' if data.get('emergency_type') else 'No'}) ---")
            print(json.dumps(data, indent=2))
            send_data(data)
            counter += 1
            time.sleep(INTERVAL_SECONDS)
        
        except KeyboardInterrupt:
            print("\nSimulator stopped by user.")
            break

if __name__ == "__main__":
    print("Waiting 3 seconds for backend to stabilize...")
    time.sleep(3)
    
    run_simulator()
