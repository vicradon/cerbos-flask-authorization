from flask import jsonify, g
from sqlalchemy.exc import IntegrityError
from app.models import User
from app.extensions import db
from app.utils.helpers import check_missing_fields

def register_user(data):
    check_missing_fields(data, ["username", "email", "password"])
    user = User(
        username=data["username"],
        email=data["email"],
    )
    user.set_password(data["password"])

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        if 'username' in str(e.orig) or 'email' in str(e.orig):
            return jsonify({"error": "Username or email already exists"}), 400
        return jsonify({"error": "An unexpected error occurred"}), 500
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred"}), 500

    return jsonify({
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "email_is_verified": user.email_is_verified
        }
    }), 201

def verify_user_email():
    user = g.user
    user.email_is_verified = True
    db.session.commit()

    return jsonify({
        "message": "User's email verified successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "email_is_verified": user.email_is_verified
        }
    })