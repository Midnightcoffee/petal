from flask import Flask
#alternative method
from flask.ext.sqlalchemy import SQLAlchemy
import os
#from  flask_heroku import Heroku

app = Flask(__name__)
#configuring from my local computer
#app.config.from_object('defaultconfig')
app.config.from_pyfile('config.py')
#app.config.from_envvar('PETAL_DEV')
# alternative method to using flask-heroku
db = SQLAlchemy(app)

#flask heroku
#heroku = Heroku(app)
#db = SQLAlchemy(app)
from petalapp import views

