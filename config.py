import os
from flask_sqlalchemy import SQLAlchemy

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = os.environ.get('SECTET_KEY') or 'testkey'

ADMIN_EMAIL = "shenmj053@163.com"

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'myfood.sqlite')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
