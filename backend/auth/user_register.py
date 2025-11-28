from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from extensions.extensions import db 
from models.models import Responder 

register_bp = Blueprint('register', __name__, url_prefix='/api/auth')

@register_bp.route('/register', methods=['POST'])
def register_user():
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Missing JSON data in request body."}), 400

        full_name = data.get('full_name')
        email = data.get('email')
        password = data.get('password')

        if not all([full_name, email, password]):
            return jsonify({"success": False, "message": "Missing required fields: full_name, email, or password."}), 400

    except Exception as e:
        return jsonify({"success": False, "message": f"Invalid JSON format: {e}"}), 400

    existing_responder_email = db.session.execute(
        db.select(Responder).filter_by(email=email)
    ).scalar_one_or_none()

    if existing_responder_email:
        return jsonify({"success": False, "message": "Responder already exists with this email address."}), 409

    new_responder = Responder(
        full_name=full_name,
        email=email,
        password=password
    )
    
    try:
        db.session.add(new_responder)
        db.session.commit()
        
        return jsonify({
            "success": True, 
            "message": "Responder registered successfully.", 
            "full_name": full_name,
            "email": email
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"success": False, "message": "Database error: Email or full name constraint violated."}), 500
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"A database error occurred: {e}"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"An unexpected error occurred during registration: {e}"}), 500