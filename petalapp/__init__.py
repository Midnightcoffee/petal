
import os
from flask import Flask
#alternative method
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from flask.ext.login import LoginManager
from config import basedir
#not sure why i would need this
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

#login setup
lm = LoginManager()
lm.setup_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))
