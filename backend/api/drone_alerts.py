from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import Responder, DroneLog, DroneStatus
from extensions.extensions import db

alerts_bp = Blueprint('alerts', __name__, url_prefix='/api')

@alerts_bp.route('/alerts', methods=['GET'])
@jwt_required()
def get_alerts():
    responder_id = get_jwt_identity()

    responder = db.session.execute(
        db.select(Responder).filter_by(responder_id=responder_id)
    ).scalar_one_or_none()
    
    if not responder:
        return jsonify({"success": False, "message": "Responder not found or invalid identity."}), 404

    drone_alerts = db.session.execute(
        db.select(DroneLog)
    ).scalars().all()

    alerts_data = []
    for alert in drone_alerts:
        alerts_data.append({
            "timestamp": alert.timestamp.isoformat(),
            "alert_id": alert.alert_id,
            "drone_id": alert.drone_id,
            "latitude": float(alert.latitude),
            "longitude": float(alert.longitude),
            "emergency_type": alert.emergency_type
        })

    return jsonify({
        "success": True,
        "responder_id": responder_id,
        "message": f"Successfully retrieved {len(alerts_data)} alerts.",
        "alerts": alerts_data
    }), 200

@alerts_bp.route('/drone/status/<string:drone_id>', methods=['GET'])
@jwt_required()
def get_drone_status(drone_id):
    
    status = db.session.execute(
        db.select(DroneStatus).filter_by(drone_id=drone_id)
    ).scalar_one_or_none()
    
    if not status:
        return jsonify({"success": False, "message": f"Status for drone {drone_id} not found."}), 404
        
    status_data = {
        "drone_id": status.drone_id,
        "timestamp": status.timestamp.isoformat(),
        "battery_percent": status.battery_percent,
        "altitude_meters": float(status.altitude_meters) if status.altitude_meters is not None else None,
        "speed_mps": float(status.speed_mps) if status.speed_mps is not None else None
    }
    
    return jsonify({
        "success": True,
        "message": f"Latest status retrieved for drone {drone_id}.",
        "status": status_data
    }), 200