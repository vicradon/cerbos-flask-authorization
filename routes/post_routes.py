from flask import Blueprint, jsonify, request
from extensions import db
from models.post import Post

post_bp = Blueprint('post_bp', __name__)

@post_bp.route('/', methods=['POST'])
def create_post():
    data = request.json
    new_post = Post(title=data['title'], content=data['content'], user_id=data['user_id'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully'}), 201

@post_bp.route('/', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{'id': post.id, 'title': post.title, 'content': post.content} for post in posts])