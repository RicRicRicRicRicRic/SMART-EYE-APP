import time
import random
import requests
from datetime import datetime

BACKEND_URL = "http://127.0.0.1:5000/log-status" 
DRONE_ID = "DRN-001"

def generate_status_data():
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    battery_percent = random.randint(30, 100)
    altitude_meters = round(random.uniform(5.0, 50.0), 2)
    speed_mps = round(random.uniform(2.0, 15.0), 2)
    
    data = {
        "drone_id": DRONE_ID,
        "timestamp": timestamp,
        "battery_percent": battery_percent,
        "altitude_meters": altitude_meters,
        "speed_mps": speed_mps
    }
    
    return data

def send_data_to_backend(data):
    try:
        response = requests.post(BACKEND_URL, json=data)
        response.raise_for_status()
        
        print(f"[{data['timestamp']}] SENT: Status: {data['battery_percent']}% Bat, {data['altitude_meters']}m Alt | Response: {response.json().get('message')}")
        
    except requests.exceptions.RequestException as e:
        print(f"[{data['timestamp']}] ERROR: Could not connect or post data to backend. Is 'backend.py' running?")
        print(f"Details: {e}")

def run_simulation(interval=1):
    print(f"--- Starting Drone Status Sender ({DRONE_ID}) ---")
    print(f"Sending status updates to {BACKEND_URL} every {interval} second. Press CTRL+C to stop.\n")
    
    try:
        while True:
            status_data = generate_status_data()
            send_data_to_backend(status_data)
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n--- Status Sender Stopped by User ---")
        
if __name__ == '__main__':
    run_simulation(interval=1)