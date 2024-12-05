from flask import jsonify, request, g
from sqlalchemy.exc import IntegrityError
from sqlalchemy.event import listen

from app.models import Post
from app.extensions import db
from app.utils.helpers import slugify, check_missing_fields
from app.utils.cerbos import get_value, check_permission, check_permission_for_resource, get_principal
from cerbos.sdk.grpc.client import CerbosClient
from cerbos.engine.v1.engine_pb2 import Resource

def set_post_slug(mapper, connection, target):
    if target.title:
        target.slug = slugify(target.title)

listen(Post, "before_insert", set_post_slug)
listen(Post, "before_update", set_post_slug)

def fetch_all_posts():
    posts = Post.query.filter_by(is_published=True).all()
    if not posts:
        return jsonify({"message": "No posts found"}), 404

    # for post in posts:
    #     if not check_permission("read", Post, post):
    #         return jsonify({"error": "You are not authorized to view this post"}), 403

    posts_data = [{
        "id": post.id,
        "title": post.title,
        "user_id": post.user_id,
        "published": post.is_published,
        "body": post.body,
        "slug": post.slug
    } for post in posts]

    return jsonify(posts_data), 200

def create_post(data):
    post_resource = Resource(id="new", kind="post")
    if not check_permission_for_resource("create", post_resource):
        return jsonify({"error": "You are not authorized to create a post"}), 403

    check_missing_fields(data, ["title", "body"])

    user = g.user

    post = Post(
        title=data["title"],
        body=data["body"]
    )

    post.user = user

    try:
        db.session.add(post)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        if 'title' in str(e.orig):
            return jsonify({"error": "Blog with this title already exists"}), 400
        return jsonify({"error": "An unexpected error occurred"}), 500

    return jsonify({
        "message": "Post created successfully",
        "post": {
            "id": post.id,
            "title": post.title,
            "published": post.is_published,
            "slug": post.slug,
        }
    }), 201

def get_post_by_id(id):
    post = Post.query.get(id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    if not check_permission("read", Post, post):
        return jsonify({"error": "You are not authorized to view this post"}), 403

    return jsonify({
        "id": post.id,
        "title": post.title,
        "published": post.is_published,
        "body": post.body,
        "slug": post.slug
    }), 200

def update_post_by_id(id, data):
    post = Post.query.get(id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    if not check_permission("update", Post, post):
        return jsonify({"error": "You are not authorized to update this post"}), 403

    check_missing_fields(data, ["title", "body"])

    post.title = data["title"]
    post.body = data["body"]
    post.slug = slugify(data["title"])

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred"}), 500

    return jsonify({
        "message": "Post updated successfully",
        "post": {
            "id": post.id,
            "title": post.title,
            "published": post.is_published,
            "slug": post.slug,
            "body": post.body
        }
    }), 200


def publish_post_by_id(id):
    post = Post.query.get(id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    if not check_permission("update", Post, post):
        return jsonify({"error": "You are not authorized to publish this post"}), 403

    post.is_published = True
    db.session.commit()

    return jsonify({
        "message": "Post published successfully",
        "post": {
            "id": post.id,
            "title": post.title,
            "published": post.is_published,
            "slug": post.slug,
        }
    }), 200


def delete_post_by_id(id):
    post = Post.query.get(id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    if not check_permission("delete", Post, post):
        return jsonify({"error": "You are not authorized to delete this post"}), 403

    db.session.delete(post)
    db.session.commit()

    return jsonify({
        "message": "Post deleted successfully"
    }), 200
