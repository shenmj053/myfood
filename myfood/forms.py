from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email,Regexp, EqualTo
from flask_pagedown.fields import PageDownField
from .models import User


class PostForm(Form):
    title = StringField('Blog Title', validators=[DataRequired()])
    body = PageDownField('Write your post body here!', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CommentForm(Form):
    body = StringField('', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(),
                                             Length(1, 64),
                                             Email()])
    nickname = StringField('Nickname', validators=[DataRequired(),
                                                   Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Nicknames must have only letters, numbers, dots or underscores')])

    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Create your account')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')