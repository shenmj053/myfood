from flask_wtf import Form
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField


class PostForm(Form):
    title = StringField('Blog Title', validators=[DataRequired()])
    body = PageDownField('Write your post body here!', validators=[DataRequired()])
    submit = SubmitField('Submit')