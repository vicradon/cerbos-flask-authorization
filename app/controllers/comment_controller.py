from flask import jsonify, request, g
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from app.models import Comment, Post, User
from app.extensions import db
from app.utils.helpers import check_missing_fields
from app.utils.cerbos import get_value, check_permission, check_permission_for_resource, get_principal
from cerbos.sdk.grpc.client import CerbosClient
from cerbos.engine.v1.engine_pb2 import Resource
from sqlalchemy.orm import lazyload, joinedload


def fetch_all_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    if not comments:
        return jsonify({"message": "No comments found"}), 404

    for comment in comments:
        if not check_permission("read", Comment, comment):
            return jsonify({"error": "You are not authorized to view this comment"}), 403

    comments_data = [{
        "id": comment.id,
        "body": comment.body,
        "user_id": comment.user_id,
    } for comment in comments]

    return jsonify(comments_data), 200

def fetch_single_comment(post_id, comment_id):
    comment = Comment.query.filter_by(post_id=post_id, id=comment_id).options(
        joinedload(Comment.user),
    ).one_or_none()

    if not comment:
        return jsonify({"message": "Comment not found"}), 404

    if not check_permission("read", Comment, comment):
        return jsonify({"error": "You are not authorized to view this comment"}), 403

    comment_data = {
        "id": comment.id,
        "body": comment.body,
        "user": {
            "id": comment.user_id,
            "username": comment.user.username,
        },
        "post_id": comment.post_id,
    }

    return jsonify(comment_data), 200

from app.utils.cerbos import get_value

def create_comment(post_id, data):
    post = Post.query.get(post_id)
    comment_resource = Resource(id="new", kind="comment", attr={"post":get_value({"is_published": post.is_published})})
    if not check_permission_for_resource("create", comment_resource):
        return jsonify({"error": "You are not authorized to create a comment"}), 403

    check_missing_fields(data, ["body"])

    comment = Comment(
        post_id=post_id,
        body=data["body"],
    )

    comment.user = g.user

    try:
        db.session.add(comment)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred"}), 500

    return jsonify({
        "message": "Comment created successfully",
        "data": {
            "body": comment.body,
            "user_id": comment.user_id,
        }
    }), 201

def update_comment_by_id(id, data):
    comment = Comment.query.get(id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    if not check_permission("update", Comment, comment):
        return jsonify({"error": "You are not authorized to update this comment"}), 403

    check_missing_fields(data, ["body"])

    comment.body = data["body"]

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred"}), 500

    return jsonify({
        "message": "Comment updated successfully",
        "data": {
            "id": comment.id,
            "body": comment.body,
            "user_id": comment.user_id,
        }
    }), 200

def delete_comment_by_id(id):
    comment = Comment.query.get(id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    if not check_permission("delete", Comment, comment):
        return jsonify({"error": "You are not authorized to delete this comment"}), 403

    db.session.delete(comment)
    db.session.commit()

    return jsonify({
        "message": "Comment deleted successfully"
    }), 200
