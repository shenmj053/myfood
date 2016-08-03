from flask import render_template
from .views import mod


@mod.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@mod.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404