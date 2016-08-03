from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown
from flask_moment import Moment


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
pagedown = PageDown(app)
bcrypt = Bcrypt(app)
moment = Moment(app)
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


from .blog.views import mod as blog_blueprint
app.register_blueprint(blog_blueprint)


from .auth.views import mod as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')