from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from kevin_map_app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username' , validators=[DataRequired(),Length(min=1, max=20)])
    password = PasswordField('Password' ,validators=[DataRequired(), Length(min=4),EqualTo('confirm_password', "Passwords must match")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()] )
    submit = SubmitField('Sign Up')
    def validate_username(self,username):
        check = User.query.filter_by(username = username.data).first()
        if check:
            raise ValidationError('Username already exists')
        

class LoginForm(FlaskForm):
    username = StringField('Username' , validators=[DataRequired(),Length(min=1, max=20)])
    password = PasswordField('Password' ,validators=[DataRequired(), Length(min=4)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')