from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_json import MutableJson

application = app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sanket:apple@123@localhost:3305/db'
app.config['SECRET_KEY'] = 'f1dcx55sfq4e78g5v5m5fg5'
db = SQLAlchemy(app)