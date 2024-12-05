from flask import Blueprint, request
from app.controllers.auth_controller import register_user, verify_user_email
from app.middleware.auth import require_auth

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    return register_user(data)

@auth_bp.route("/verify-email", methods=["POST"])
@require_auth
def verify_email():
    return verify_user_email()

