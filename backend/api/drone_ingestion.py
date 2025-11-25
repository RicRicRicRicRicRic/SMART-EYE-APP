from flask import Blueprint, request, jsonify
from extensions.extensions import db
from models.models import DroneLog, DroneStatus
from datetime import datetime
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

drone_bp = Blueprint('drone', __name__, url_prefix='/api/drone')

DRONE_API_KEY = "SUPER_SECRET_DRONE_KEY" 

def check_drone_key(key):
    return key == DRONE_API_KEY

@drone_bp.route('/data', methods=['POST'])
def receive_drone_data():
    api_key = request.headers.get('X-Drone-API-Key')
    if not check_drone_key(api_key):
        return jsonify({"success": False, "message": "Unauthorized: Invalid Drone API Key."}), 401

    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Missing JSON data."}), 400

        drone_id = data.get('drone_id')
        timestamp_str = data.get('timestamp')

        if not drone_id or not timestamp_str:
            return jsonify({"success": False, "message": "Missing required fields: drone_id or timestamp."}), 400

        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')) 
        except ValueError:
            return jsonify({"success": False, "message": "Invalid timestamp format. Use ISO 8601."}), 400

        new_status = DroneStatus(
            drone_id=drone_id,
            timestamp=timestamp,
            battery_percent=data.get('battery_percent'),
            altitude_meters=data.get('altitude_meters'),
            speed_mps=data.get('speed_mps')
        )
        
        db.session.merge(new_status)
        
        status_message = "Status updated."

        alert_log = None
        if data.get('emergency_type'):
            alert_id = data.get('alert_id')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            
            if not all([alert_id, latitude, longitude]):
                return jsonify({"success": False, "message": "Missing required alert fields: alert_id, latitude, or longitude."}), 400

            alert_log = DroneLog(
                timestamp=timestamp,
                alert_id=alert_id,
                drone_id=drone_id,
                latitude=latitude,
                longitude=longitude,
                emergency_type=data.get('emergency_type')
            )
            db.session.add(alert_log)
            status_message += " Alert logged."
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": status_message,
            "drone_id": drone_id,
            "timestamp": timestamp_str
        }), 201

    except (IntegrityError, SQLAlchemyError) as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"A database error occurred: {e}"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"An unexpected error occurred during data processing: {e}"}), 500