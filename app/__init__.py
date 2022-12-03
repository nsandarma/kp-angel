from flask import Flask,render_template,redirect,request,session,url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'WEB-BMKG'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'




db = SQLAlchemy(app)

with app.app_context():
    db.create_all()




from app.saw import *
from app.models import *
from app.routes import *
