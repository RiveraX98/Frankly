from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, TextAreaField, EmailField
from wtforms.validators import InputRequired, Email


class RegistrationForm(FlaskForm):
    first_name = StringField("First name:", validators=[InputRequired()])
    last_name = StringField("Last name:", validators=[InputRequired()])
    email = EmailField("Email:", validators=[InputRequired()])
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])


class loginForm(FlaskForm):
    username = StringField("username:", validators=[InputRequired()])
    password = PasswordField("password:", validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    title = StringField("Title:")
    content = TextAreaField("Feedback:", validators=[InputRequired()])
