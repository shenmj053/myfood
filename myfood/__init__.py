from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown
from flask_moment import Moment
from config import config


db = SQLAlchemy()
bootstrap = Bootstrap()
pagedown = PageDown()
bcrypt = Bcrypt()
moment = Moment()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)
    pagedown.init_app(app)
    bcrypt.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

    from .blog.views import mod as blog_blueprint
    app.register_blueprint(blog_blueprint)


    from .auth.views import mod as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app