import sqlite3
import json
from flask import Flask, request, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

DATABASE = 'smart_eye.db'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_very_secret_key_that_should_be_long_and_random' 

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drone_logs (
                timestamp DATETIME NOT NULL,
                alert_id INTEGER NOT NULL,
                drone_id TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                emergency_type TEXT,
                PRIMARY KEY (timestamp, alert_id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drone_status (
                drone_id TEXT NOT NULL PRIMARY KEY,
                timestamp DATETIME NOT NULL,
                battery_percent INTEGER,
                altitude_meters REAL,
                speed_mps REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

        try:
            cursor.execute("ALTER TABLE drone_logs ADD COLUMN emergency_type TEXT")
            print("Successfully added column 'emergency_type' to drone_logs.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e):
                raise e
            
        db.commit()
        print("Database schema ensured.")

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required.'}), 400

    hashed_password = generate_password_hash(password)

    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, hashed_password)
        )
        db.commit()
        
        user_id = cursor.lastrowid
        
        return jsonify({'message': 'User registered successfully.', 'user_id': user_id}), 201

    except sqlite3.IntegrityError:
        return jsonify({'message': 'Registration failed: Email already exists.'}), 409
    except Exception as e:
        print(f"Error during user registration: {e}")
        return jsonify({'message': 'An internal server error occurred.'}), 500

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Missing email or password.'}), 400

    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT user_id, email, password FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({'message': 'Login failed: User not found.'}), 401

    hashed_password = user['password']
    if check_password_hash(hashed_password, password):
        try:
            payload = {
                'user_id': user['user_id'],
                'email': user['email'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24) 
            }
            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
            
            return jsonify({
                'message': 'Login successful.',
                'token': token
            }), 200
        except Exception as e:
            print(f"Error generating token: {e}")
            return jsonify({'message': 'Could not generate authentication token.'}), 500
    else:
        return jsonify({'message': 'Login failed: Incorrect password.'}), 401


@app.route('/log-alert', methods=['POST'])
def log_alert():
    data = request.get_json()
    
    required_fields = ['drone_id', 'alert_id', 'timestamp', 'location']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields in payload.'}), 400
    
    drone_id = data.get('drone_id')
    alert_id = data.get('alert_id')
    timestamp = data.get('timestamp')
    location = data.get('location', {})
    
    latitude = location.get('latitude')
    longitude = location.get('longitude')
    
    emergency_type = data.get('emergency_type', None)

    if latitude is None or longitude is None:
        return jsonify({'message': 'Latitude or Longitude is missing from location.'}), 400
    
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute(
            "INSERT INTO drone_logs (timestamp, alert_id, drone_id, latitude, longitude, emergency_type) VALUES (?, ?, ?, ?, ?, ?)",
            (timestamp, alert_id, drone_id, latitude, longitude, emergency_type)
        )
        db.commit()
        
        return jsonify({'message': 'Drone alert logged successfully.', 'alert_id': alert_id}), 200

    except sqlite3.IntegrityError:
        return jsonify({'message': 'Data log failed: Duplicate entry detected.'}), 409
    except Exception as e:
        print(f"Error logging drone data: {e}")
        return jsonify({'message': 'An internal server error occurred.'}), 500

@app.route('/log-status', methods=['POST'])
def log_status():
    data = request.get_json()
    
    required_fields = ['drone_id', 'timestamp', 'battery_percent', 'altitude_meters', 'speed_mps']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields in payload.'}), 400
    
    drone_id = data.get('drone_id')
    timestamp = data.get('timestamp')
    battery_percent = data.get('battery_percent')
    altitude_meters = data.get('altitude_meters')
    speed_mps = data.get('speed_mps')
    
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute(
            "INSERT OR REPLACE INTO drone_status (drone_id, timestamp, battery_percent, altitude_meters, speed_mps) VALUES (?, ?, ?, ?, ?)",
            (drone_id, timestamp, battery_percent, altitude_meters, speed_mps)
        )
        db.commit()
        
        return jsonify({'message': 'Drone status logged successfully.', 'drone_id': drone_id}), 200

    except Exception as e:
        print(f"Error logging drone status: {e}")
        return jsonify({'message': 'An internal server error occurred.'}), 500

with app.app_context():
    init_db()

if __name__ == '__main__':
    print("\n--- Smart Eye Backend Server Starting ---")
    print("NOTE: Requires 'PyJWT' for authentication.")
    print("Database: smart_eye.db")
    print("Endpoints: /register (POST), /login (POST), /log-alert (POST), /log-status (POST) are ready.")
    app.run(debug=True)