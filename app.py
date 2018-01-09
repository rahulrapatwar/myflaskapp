from flask import Flask, render_template, flash, redirect, request, url_for, session, logging
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' # Returns in the form of dictionary

# Init MySQL
mysql = MySQL(app)

Articles = Articles()

# Home page view
@app.route('/')
def index():
    return render_template('home.html')

# About Us page
@app.route('/about')
def about():
    return render_template('about.html')

# Articles page
@app.route('/articles')
def articles():
    return render_template('articles.html',articles = Articles)

# Article detail page
@app.route('/article/<string:id>')
def article(id):
    return render_template('article.html',id=id)

# Register form class
class RegisterForm(Form):
    name = StringField('Name',[validators.Length(min=2,max=50)])
    email = StringField('Email',[validators.Length(min=6,max=50)])
    username = StringField('Username',[validators.Length(min=4,max=50)])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm',message='The password does not match')
    ])
    confirm = PasswordField('Confirm Password')

# Register page
@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        pass
    return render_template('register.html',form = form)

if __name__ == '__main__':
    app.run(debug=True)
