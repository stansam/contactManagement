from flask_mail import Mail
from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from flask_login import LoginManager

mail = Mail()
login_manager = LoginManager()

# Token serializer for password reset
serializer = URLSafeTimedSerializer