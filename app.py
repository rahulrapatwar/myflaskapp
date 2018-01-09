from flask import Flask, render_template
from data import Articles

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
