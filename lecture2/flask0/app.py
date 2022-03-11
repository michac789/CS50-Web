"""
Flask 0: Getting Started with Flask

- Use 'pip install flask' to first download flask
- Create app.py (main file) and type flask run in the correct directory
- On the terminal, type 'set FLASK_APP = app.py' (by default)
- Basic format for app.py is as shown below
- Type @app.route('path') for different paths
- Create 'templates' folder for all html files
- Use 'render_template' function from flask to render html
"""
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", name="world")

@app.route('/<string:name>')
def greet(name):
    return render_template("index.html", name=name)

@app.route('/print/<string:text>')
def print(text):
    return f"Printout: {text}"
