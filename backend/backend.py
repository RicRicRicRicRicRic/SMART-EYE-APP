import sqlite3
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

DATABASE = 'smart_eye.db'

def init_db():
    """Initializes the SQLite database and creates the necessary tables."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drones (
                id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                alerts TEXT
            )
        ''')
        # Check if the "dummy" drone already exists, if not, create it.
        cursor.execute('SELECT * FROM drones WHERE id = "drone1"')
        if cursor.fetchone() is None:
            initial_alerts = json.dumps([])
            cursor.execute('INSERT INTO drones (id, status, latitude, longitude, alerts) VALUES (?, ?, ?, ?, ?)',
                           ('drone1', 'Idle', 34.0522, -118.2437, initial_alerts))
        conn.commit()

# Call the function to initialize the database when the server starts
init_db()

@app.route("/")
def home():
    """A simple home endpoint to confirm the server is running."""
    return "<h1>Smart Eye Backend</h1><p>Server is running. Please use the /drone-status and /drone-update endpoints.</p>"

@app.route("/drone-status", methods=["GET"])
def get_drone_status():
    """
    Returns the current status of the drone by fetching it from the database.
    This is the endpoint the Flutter app will call to get the data.
    """
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM drones WHERE id = "drone1"')
        row = cursor.fetchone()
        conn.close()

        if row:
            # Reconstruct the drone data from the database row
            drone_data = {
                "id": row[0],
                "status": row[1],
                "latitude": row[2],
                "longitude": row[3],
                "alerts": json.loads(row[4])
            }
            return jsonify(drone_data)
        else:
            return jsonify({"message": "Drone not found"}), 404
    except sqlite3.Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500

@app.route("/drone-update", methods=["POST"])
def update_drone_status():
    """
    Receives updates from the drone (or a simulator) and saves them to the database.
    """
    update = request.get_json()
    if not update or 'id' not in update:
        return jsonify({"message": "Invalid update data. 'id' is required."}), 400

    drone_id = update['id']
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Check if the drone exists
        cursor.execute('SELECT * FROM drones WHERE id = ?', (drone_id,))
        existing_data = cursor.fetchone()
        
        if existing_data:
            # If the drone exists, get its current alerts and update all fields
            current_alerts = json.loads(existing_data[4])
            if "alerts" in update and isinstance(update["alerts"], list):
                current_alerts.extend(update["alerts"])

            cursor.execute('''
                UPDATE drones
                SET status = ?, latitude = ?, longitude = ?, alerts = ?
                WHERE id = ?
            ''', (update.get("status", existing_data[1]),
                  update.get("latitude", existing_data[2]),
                  update.get("longitude", existing_data[3]),
                  json.dumps(current_alerts),
                  drone_id))
        else:
            # If the drone doesn't exist, create a new record
            alerts_to_add = json.dumps(update.get("alerts", []))
            cursor.execute('''
                INSERT INTO drones (id, status, latitude, longitude, alerts)
                VALUES (?, ?, ?, ?, ?)
            ''', (drone_id,
                  update.get("status", "Idle"),
                  update.get("latitude", 0.0),
                  update.get("longitude", 0.0),
                  alerts_to_add))

        conn.commit()
        conn.close()
        return jsonify({"message": "Drone data updated successfully"}), 200

    except sqlite3.Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
