from flask import Flask, render_template, flash, redirect, request, url_for, session, logging
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' # Returns in the form of dictionary

# Init MySQL
mysql = MySQL(app)

# Articles = Articles()

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
    # Create cursor
    cur = mysql.connection.cursor()
    # Get articles
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()

    if result > 0: # If articles exists
        return render_template('articles.html', articles = articles)
    else:
        msg = "No Articles Found"
        return render_template('articles.html', msg=msg)
    # Close connection
    cur.close()

# Article detail page
@app.route('/article/<string:id>')
def article(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Query for username entered
    result = cur.execute("SELECT * FROM articles WHERE id=%s",[id])
    if result > 0:
        article = cur.fetchone()


    return render_template('article.html',article=article)

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
        # Fetching data from the form
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data)) # Encrypting the password before storing to the database

        # Create cursor
        cur = mysql.connection.cursor()
        # Executing the query
        cur.execute("INSERT INTO users(name,email,username,password) VALUES(%s,%s,%s,%s)", (name,email,username,password))
        # Commit to database
        mysql.connection.commit()
        # Close connection
        cur.close()
        # Success flash
        flash('You are successfully registered and you can now login','success')
        return redirect(url_for('index'))
    return render_template('register.html',form = form)

# Login page
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST': # POST request
        # Get data from the form
        username = request.form['username']
        password_user = request.form['password']
        # Create cursor
        cur = mysql.connection.cursor()
        # Query for username entered
        result = cur.execute("SELECT * FROM users WHERE username=%s",[username])

        if result > 0: # Record found
            # Get stored hash
            data = cur.fetchone()
            password = data['password'] # data is in the dictionary format and fetching the password
            # Compare passwords
            if sha256_crypt.verify(password_user,password): # If both passwords match
                # Create session
                session['logged_in'] = True
                session['username'] = username

                flash("You are now logged in",'success')
                return redirect(url_for('dashboard'))
            else:
                error = "Invalid login"
                return render_template('login.html',error=error)
        else: # Username does not exits in the database
            error = "User does not exist"
            return render_template('login.html',error=error)
    # GET request
    return render_template('login.html')

# Login check
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash("Unauthorized, please login", 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been successfully logged out",'success')
    return redirect(url_for('login'))

# Dashboard page
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    cur = mysql.connection.cursor()
    # Get articles
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()

    if result > 0: # If articles exists
        return render_template('dashboard.html', articles = articles)
    else:
        msg = "No Articles Found"
        return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()

# Article form class
class ArticleForm(Form):
    title = StringField('Title',[validators.Length(min=2,max=200)])
    body = TextAreaField('Body',[validators.Length(min=20)])

# Add Article
@app.route('/add_article', methods=['GET','POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        # Create cursor
        cur = mysql.connection.cursor()
        # Executing the query
        cur.execute("INSERT INTO articles(title,body,author) VALUES(%s,%s,%s)", (title,body,session['username']))
        # Commit to database
        mysql.connection.commit()
        # Close connection
        cur.close()
        # Success flash
        flash("Article created",'success')
        return redirect(url_for('dashboard'))
    return render_template('add_article.html',form=form)


if __name__ == '__main__':
    app.secret_key = 'Secret123'
    app.run(debug=True)
