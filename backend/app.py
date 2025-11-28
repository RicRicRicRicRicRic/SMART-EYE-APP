from flask import Flask
from config.config import get_config
from extensions.extensions import db
from models.models import Responder, DroneLog, DroneStatus
from auth.user_register import register_bp
from auth.user_auth import login_bp
from api.drone_alerts import alerts_bp
from api.drone_ingestion import drone_bp
from flask_jwt_extended import JWTManager

config = get_config()
app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

jwt = JWTManager(app)

app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(alerts_bp)
app.register_blueprint(drone_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 

    app.run(port=app.config['APP_PORT'], debug=app.config['DEBUG'])