from flask import Flask, render_template
from config import Config
import os

from app.extensions import db, login, migrate, bootstrap  # NEW
from flask_login import LoginManager  # you can drop this if you use `login` only

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')

    from app.comments import bp as comments_bp
    app.register_blueprint(comments_bp, url_prefix='/comments')

    with app.app_context():
        if os.environ.get("FLASK_RUN_CREATE_ALL") == "1":
            db.create_all()

    from app.models import User, Post, Comment  # import AFTER db is ready

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'Post': Post, 'Comment': Comment}

    return app