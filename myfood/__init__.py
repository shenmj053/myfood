from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
pagedown = PageDown(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


from .views import home, auth
app.register_blueprint(home.mod)
app.register_blueprint(auth.mod, url_prefix='/auth')