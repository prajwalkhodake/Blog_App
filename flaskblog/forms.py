from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flaskblog.models import User



class registrationFrom (FlaskForm):

    username = StringField('Username', [DataRequired(), Length(2, 20)])
    
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
    confirm_password = PasswordField('Confirm Password', [DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is not available !')
        
    def validate_email(self, email):
        
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Already have account with this email !')


class loginFrom (FlaskForm):
    
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')