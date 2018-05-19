from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(Form):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password',
                                                 message='Password do not match')])
    # submit = SubmitField('Sign Up')



# Article Form Class
class PostForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    content = TextAreaField('Content', [validators.Length(min=30)])