from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Initialize SQLAlchemy instance for database integration
db = SQLAlchemy()  # Initialized without app

# Initialize Migrate instance for database migration management
migrate = Migrate()  # Initialized without app

def create_app():
    """
    Factory function to create and configure the Flask application.

    Returns:
        Flask: Configured instance of the Flask application.
    """
    
    # Create Flask app instance
    app = Flask(__name__)
    
    # Set secret key for session management (use a strong, unique value)
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    
    # Set the database URI for SQLAlchemy (in this case SQLite)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    
    # Enable Cross-Origin Resource Sharing (CORS) for the app
    CORS(app)

    # Bind the database and app instances for SQLAlchemy
    db.init_app(app)

    # Bind the migrate instance to the app and database for easy migrations
    migrate.init_app(app, db)

    # Import and register blueprints for route management
    # In this case, it's a blueprint from 'views' named 'security_bp'
    from .views import security_bp
    app.register_blueprint(security_bp)  # Register without url_prefix to avoid the "security" prefix in routes

    app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  
    jwt = JWTManager(app)  

    # Automatically create tables if they don't exist
    with app.app_context():
        db.create_all()

    # Return the configured app instance
    return app