from .post_routes import post_bp
from .auth_routes import auth_bp
from .base_route import base_bp

def register_routes(app):
    app.register_blueprint(base_bp)
    app.register_blueprint(post_bp, url_prefix='/posts')
    app.register_blueprint(auth_bp, url_prefix='/auth')