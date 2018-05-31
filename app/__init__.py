from flask import Flask,request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)

from app import routes, models
