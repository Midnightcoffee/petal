from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('defaultconfig')
app.config.from_envvar('PETAL_DEV')
db = SQLAlchemy(app)

from petalapp import views


