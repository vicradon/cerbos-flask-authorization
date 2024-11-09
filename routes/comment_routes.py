from flask import Blueprint, jsonify, request
from extensions import db
from models.comment import Comment

comment_bp = Blueprint('comment_bp', __name__)

@comment_bp.route('/', methods=['POST'])
def create_comment():
    data = request.json
    new_comment = Comment(content=data['content'], user_id=data['user_id'], post_id=data['post_id'])
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'message': 'Comment created successfully'}), 201

@comment_bp.route('/', methods=['GET'])
def get_comments():
    comments = Comment.query.all()
    return jsonify([{'id': comment.id, 'content': comment.content, 'user_id': comment.user_id, 'post_id': comment.post_id} for comment in comments])