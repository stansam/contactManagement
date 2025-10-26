import os
from flask import Flask, render_template, request
from flask_login import current_user
from logging.handlers import RotatingFileHandler

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)

    # Logging setup 
    from app.settings.logs import init_logs
    init_logs()
    
    # Config setup
    from app.settings.config import Config
    app.config.from_object(Config)
    
    # Initialize extensions
    from app.settings.extensions import login_manager, mail, serializer
    from app.settings.database import Database
    
    mail.init_app(app)
    Database.initialize()
    serializer(app.config['SECRET_KEY'])
    
    # Configure Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        user_data = User.get_by_id(user_id)
        if user_data:
            user_data['_id'] = str(user_data['_id'])
            return User(user_data)
        return None

    
    # Register blueprints
    from app.settings.blueprints import register_blueprints
    register_blueprints(app)

    
    return app

from app import models