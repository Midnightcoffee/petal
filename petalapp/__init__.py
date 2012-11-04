from flask import Flask
#alternative method
from flask.ext.sqlalchemy import SQLAlchemy
#import os
from  flask_heroku import Heroku

app = Flask(__name__)
#configuring from my local computer
#app.config.from_object('defaultconfig')
app.config.from_pyfile('fakeconfig.py')
app.config.from_envvar('PETAL_PRO')
# alternative method to using flask-heroku
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']


#flask heroku
heroku = Heroku(app)
db = SQLAlchemy(app)
from petalapp import views


