from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask import redirect, render_template, request, session
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET')
db = SQLAlchemy(app)


@app.route("/")
def index():
    return "Projektinator is running, wooohoo!"
