from wtforms.validators import DataRequired,Length,EqualTo
from wtforms import StringField,PasswordField,SubmitField,Form
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
app = Flask(__name__)
class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired(message="Boş bırakılamaz")])
    password = PasswordField("Password", validators=[DataRequired(message="Boş bırakılamaz")])
    

class RegisterForm(Form):
    username = StringField('Username',validators=[DataRequired(message="Boş bırakılamaz"), Length(6,15)])
    password = PasswordField('Password',validators=[DataRequired(message="Boş bırakılamaz"),Length(min=8)])
    conf_password = PasswordField('Confirm Password',validators=[DataRequired(message="Boş bırakılamaz"),EqualTo('password','passwords are must be same')])


    def validate(self, extra_validators=None):
        return super().validate()
    
