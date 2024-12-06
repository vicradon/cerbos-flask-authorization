class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # SQLite configuration
    # SQLALCHEMY_DATABASE_URI = 'postgresql://cerbos_flask_auth:nights-once-days-forever@localhost:5432/cerbos_flask_auth'  # PostgreSQL configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STRICT_SLASHES = False