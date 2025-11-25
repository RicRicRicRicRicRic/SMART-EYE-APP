from extensions.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Responder(db.Model):
    __tablename__ = 'responder'

    responder_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    salt = db.Column(db.String(255), nullable=True)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, full_name, email, password):
        self.full_name = full_name
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Responder {self.email}>'

class DroneLog(db.Model):
    __tablename__ = 'drone_logs'
    
    # Removed (fsp=0) to fix TypeError
    timestamp = db.Column(db.DateTime, primary_key=True, nullable=False)
    alert_id = db.Column(db.Integer, primary_key=True, autoincrement=False, nullable=False) 
    
    drone_id = db.Column(db.String(50), nullable=False, index=True)
    latitude = db.Column(db.Numeric(10, 6), index=True)
    longitude = db.Column(db.Numeric(10, 6), index=True)
    emergency_type = db.Column(db.String(100))

    def __repr__(self):
        return f'<DroneLog Alert:{self.alert_id} Drone:{self.drone_id}>'

class DroneStatus(db.Model):
    __tablename__ = 'drone_status'
    
    drone_id = db.Column(db.String(50), primary_key=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, index=True)
    battery_percent = db.Column(db.SmallInteger)
    altitude_meters = db.Column(db.Numeric(5, 2))
    speed_mps = db.Column(db.Numeric(5, 2))

    def __repr__(self):
        return f'<DroneStatus Drone:{self.drone_id} Battery:{self.battery_percent}%>'