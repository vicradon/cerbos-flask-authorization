from functools import wraps
from flask import request, jsonify, g
from werkzeug.security import check_password_hash
import base64

from app.extensions import db
from app.models import User

def require_auth(f):
    @wraps(f)
    def inner_function(*args, **kwargs):
        username, password = None, None
        
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Basic "):
            try:
                auth_encoded = auth_header.split(" ", 1)[1]
                auth_decoded = base64.b64decode(auth_encoded).decode("utf-8")
                username, password = auth_decoded.split(":", 1)
            except Exception:
                return jsonify({"error": "Unauthorized: Invalid Authorization header"}), 401
        
        if not username or not password:
            auth_data = request.authorization 
            if auth_data:
                username = auth_data.username
                password = auth_data.password

        if not username or not password:
            return jsonify({"error": "Unauthorized: Missing credentials"}), 401
        
        if not validate_user(username, password):
            return jsonify({"error": "Unauthorized: Invalid username or password"}), 401

        return f(*args, **kwargs)
    return inner_function

def validate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        g.user = user
        return user.check_password(password)

    return False