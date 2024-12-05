from flask import Blueprint

base_bp = Blueprint('base_bp', __name__)

@base_bp.route("/", methods=["GET"])
def get_root():
    return "Hello Cerbos Flask!"
