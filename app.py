from flask import Flask, render_template

app = Flask(__name__)

# Home page view
@app.route('/')
def index():
    return render_template('home.html')

# About Us page
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
