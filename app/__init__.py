from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_migrate import Migrate  # <-- Add this import
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap5()
migrate = Migrate()  # <-- Add this

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)  # <-- Add this

    login_manager.login_view = 'main.login'  # Redirect to login if not authenticated

    from .models import User  # Import here to avoid circular imports

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Remove db.create_all() when using migrations!
    # with app.app_context():
    #     db.create_all()  # Create tables if they don't exist

    return app 