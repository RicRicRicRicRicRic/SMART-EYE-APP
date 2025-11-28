from flask import Blueprint, request, jsonify
from extensions.extensions import db 
from models.models import Responder
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from datetime import timedelta
import os

login_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@login_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Missing JSON data in request body."}), 400

        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return jsonify({"success": False, "message": "Missing required fields: email or password."}), 400

    except Exception:
        return jsonify({"success": False, "message": "Invalid JSON format."}), 400

    responder = db.session.execute(
        db.select(Responder).filter_by(email=email)
    ).scalar_one_or_none()

    if responder is None:
        return jsonify({"success": False, "message": "Invalid credentials."}), 401
    
    if not responder.check_password(password):
        return jsonify({"success": False, "message": "Invalid credentials."}), 401

    if not responder.is_active:
        return jsonify({"success": False, "message": "Account is inactive. Please contact support."}), 403

    access_token = create_access_token(
        identity=responder.responder_id, 
        expires_delta=timedelta(minutes=30)
    )

    return jsonify({
        "success": True,
        "message": "Login successful.",
        "access_token": access_token,
        "user_id": responder.responder_id
    }), 200