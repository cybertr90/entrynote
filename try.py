from flask_wtf.form import _Auto
from wtforms import Form,  StringField, PasswordField, validators, TextAreaField
from flask import Flask, render_template, request,flash,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.orm import relationship
from flask_babel import gettext as _lg
from datetime import datetime



app = Flask(__name__)
db = SQLAlchemy()   
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.secret_key = "developerkey"

class User(db.Model):
    __tablename__ = "persons"
    user_id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(20),nullable=False)
    password = db.Column(db.String(20),nullable=False)
    notes = relationship('Notes',backref="User")
    def __repr__(self):
        return f"User {self.username}"
    

class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer(),primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('persons.user_id'), nullable=False)
    persons = relationship('User',uselist=False,backref="Notes")
    note = db.Column(db.String(200))
    rightnow_date = db.Column(db.Date())
    

db.init_app(app)

with app.app_context():
    db.create_all()


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Re-Enter Password')
#Home
@app.route("/")
def home():
    return render_template('home.html')
   
#Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data,
                    password=form.password.data)
        
        exist_user = User.query.filter_by(username=form.username.data).first()
        if exist_user:
            raise BaseException("this username already exist")
       
        db.session.add(user)
        db.session.commit()        
        return redirect(url_for('login'))
    
        
    return render_template('register.html', form=form)
#Login
class LoginForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        db.session.begin()
        validate_user = db.session.execute(text(f"SELECT * FROM persons WHERE username = '{username}' AND password = '{password}'")).scalar()
        db.session.commit()
        user_id = validate_user
        if validate_user:
            session['username'] = username
            session['user_id'] = user_id
            print(session['username'],session['user_id'])
            return redirect(url_for("profile"))
        

            
        if not validate_user:
            flash("incorrect username or password")

        
    return render_template('login.html',form=form)

#Profile

@app.route("/profile", methods=['GET','POST'])
def profile():
        
    class EntryNote(Form):
        
            from wtforms.validators import Length
            note = TextAreaField('Enter anything', validators=[Length(max=200)])
            

    noteForm = EntryNote(request.form)

    user_id = session.get('user_id')
    if request.method == 'POST' and noteForm.validate():
        
        
        note = noteForm.note.data
        add_note = Notes(user_id=user_id, note=note,rightnow_date=datetime.utcnow())
        db.session.add(add_note)
        db.session.commit()
    
    get_note = Notes.query.filter_by(user_id=user_id).all()


    return render_template(
    "profile.html",
    noteform = noteForm,
    username = session['username'], 
    note = get_note,
    lg = _lg)



if __name__ == "__main__":
    app.run(debug=True)
