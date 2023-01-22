from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


"""
Setup:
1. Create project directory
2. cd into project directory
3. Create virtual environment
    a. $conda create flask_env
    b. $conda activate flask_env
    c. $conda install Flask
4. Create flask hello world python file in project directory
5. Paste in minimal hello world code from Flask quickstart guide
    a. https://flask.palletsprojects.com/en/2.2.x/quickstart/
6. Export flask app variable for linux system
    a. $export FLASK_APP=flask_hello_world.py
7. flask run
"""