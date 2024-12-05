from flask import Blueprint, jsonify, request
from app.controllers.post_controller import (
    fetch_all_posts, 
    create_post, 
    get_post_by_id, 
    update_post_by_id,
    publish_post_by_id,
    delete_post_by_id
)

from app.controllers.comment_controller import (
    fetch_all_comments,
    fetch_single_comment,
    create_comment,
    update_comment_by_id,
    delete_comment_by_id
)

from app.middleware.auth import require_auth

post_bp = Blueprint('post_bp', __name__)

@post_bp.route("/", methods=["GET"])
@require_auth
def get_all_posts():
    return fetch_all_posts()

@post_bp.route("/", methods=["POST"])
@require_auth
def create_blog_post():
    data = request.get_json()
    return create_post(data)

@post_bp.route("/<int:id>", methods=["GET"])
@require_auth
def get_post(id):
    return get_post_by_id(id)

@post_bp.route("/<int:id>", methods=["PUT"])
@require_auth
def update_post(id):
    data = request.get_json()
    return update_post_by_id(id, data)


@post_bp.route("/<int:id>/publish", methods=["PUT"])
@require_auth
def publish_post(id):
    return publish_post_by_id(id)

@post_bp.route("/<int:id>", methods=["DELETE"])
@require_auth
def delete_post(id):
    return delete_post_by_id(id)

@post_bp.route("/<int:post_id>/comments", methods=["GET"])
@require_auth
def get_comments(post_id):
    return fetch_all_comments(post_id)

@post_bp.route("/<int:post_id>/comments/<int:comment_id>", methods=["GET"])
@require_auth
def get_single_comment(post_id, comment_id):
    return fetch_single_comment(post_id, comment_id)

@post_bp.route("/<int:post_id>/comments", methods=["POST"])
@require_auth
def add_comment(post_id):
    data = request.get_json()
    return create_comment(post_id, data)

@post_bp.route("/comments/<int:id>", methods=["PUT"])
@require_auth
def update_comment(id):
    data = request.get_json()
    return update_comment_by_id(id, data)

@post_bp.route("/comments/<int:id>", methods=["DELETE"])
@require_auth
def delete_comment(id):
    return delete_comment_by_id(id)
