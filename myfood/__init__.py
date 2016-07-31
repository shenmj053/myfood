from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
pagedown = PageDown(app)


from .views import home
app.register_blueprint(home.mod)