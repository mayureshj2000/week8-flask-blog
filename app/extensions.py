from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()
bootstrap = Bootstrap()