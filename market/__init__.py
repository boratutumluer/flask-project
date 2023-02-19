import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.app_context().push()
# DB Connection and Configs
secret_key = os.urandom(12).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:bora00254613@localhost/flask'
app.config['SECRET_KEY'] = secret_key
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
from market import routes


