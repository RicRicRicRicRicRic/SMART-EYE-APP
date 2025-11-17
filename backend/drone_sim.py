import time
import random
import requests
import json
from datetime import datetime

BACKEND_URL = "http://127.0.0.1:5000/log-alert" 
BASE_LATITUDE = 14.5995 
BASE_LONGITUDE = 120.9842
DRONE_ID = "DRN-001"
EMERGENCY_TYPES = ["vehicle accident", "dog attack", "unintentional injuries"]

def generate_drone_data():
    
    latitude = BASE_LATITUDE + random.uniform(-0.001, 0.001)
    longitude = BASE_LONGITUDE + random.uniform(-0.001, 0.001)
    
    alert_id = random.randint(100000, 999999)
    
    emergency_type = random.choice(EMERGENCY_TYPES)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "drone_id": DRONE_ID,
        "alert_id": alert_id,
        "timestamp": timestamp,
        "emergency_type": emergency_type,
        "location": {
            "latitude": round(latitude, 6),
            "longitude": round(longitude, 6)
        }
    }
    
    return data

def send_data_to_backend(data):
    try:
        response = requests.post(BACKEND_URL, json=data)
        response.raise_for_status() 
        
        print(f"[{data['timestamp']}] SENT: Alert {data['alert_id']} ({data['emergency_type']}) | Backend Response: {response.json().get('message')}")
        
    except requests.exceptions.RequestException as e:
        print(f"[{data['timestamp']}] ERROR: Could not connect or post data to backend. Is 'backend.py' running?")
        print(f"Details: {e}")

def run_simulation(interval=3):
    print(f"--- Starting Drone Simulator ({DRONE_ID}) ---")
    print(f"Sending data to {BACKEND_URL} every {interval} seconds. Types: {', '.join(EMERGENCY_TYPES)}. Press CTRL+C to stop.\n")
    
    try:
        while True:
            drone_data = generate_drone_data()
            send_data_to_backend(drone_data)
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n--- Simulation Stopped by User ---")
        
if __name__ == '__main__':
    run_simulation(interval=3)