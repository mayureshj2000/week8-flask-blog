from flask import Flask, render_template
from config import Config
import os

from app.extensions import db, login, migrate, bootstrap


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    # Configure the SAME LoginManager instance that has @login.user_loader
    login.login_view = 'auth.login'
    login.login_message = 'Please log in to access this page.'

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
        from app.models import User, Post, Comment  # ensure models (and @login.user_loader) are imported

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