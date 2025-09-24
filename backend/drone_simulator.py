import requests
import time
import json
import random

def simulate_drone_updates():
    """
    This function acts as a simple drone simulator, sending data to the backend.
    """
    drone_id = "drone1"
    
    print("Starting drone simulator...")

    while True:
        try:
            latitude = 34.0522 + random.uniform(-0.01, 0.01)
            longitude = -118.2437 + random.uniform(-0.01, 0.01)
            
            alerts = []
            if random.random() > 0.8:
                alerts.append(f"Obstacle detected at [{time.strftime('%Y-%m-%d %H:%M:%S')}]")
            
            statuses = ["Idle", "In-Flight", "Returning", "Emergency"]
            status = random.choice(statuses)

            payload = {
                "id": drone_id,
                "status": status,
                "latitude": latitude,
                "longitude": longitude,
                "alerts": alerts
            }

            response = requests.post("http://127.0.0.1:5000/drone-update", json=payload)
            response.raise_for_status() 

            print(f"Update sent successfully: {response.json()}")

        except requests.exceptions.RequestException as e:
            print(f"Error sending update: {e}")
        

        time.sleep(3)

if __name__ == "__main__":
    simulate_drone_updates()
