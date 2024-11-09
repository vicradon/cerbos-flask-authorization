from .user_routes import user_bp
from .post_routes import post_bp
from .comment_routes import comment_bp

def register_routes(app):
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(post_bp, url_prefix='/posts')
    app.register_blueprint(comment_bp, url_prefix='/comments')