from flask import Flask
app = Flask(__name__)
app.config.from_pyfile('config.py')

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask.ext.login import LoginManager
from flask_principal import Principal
lm = LoginManager()
lm.init_app(app)
principles = Principal(app)

from flask.ext.browserid import BrowserID
from browserid_tools import get_user_by_id, get_user
login_manager = LoginManager()
login_manager.user_loader(get_user_by_id)
login_manager.init_app(app)
browserid = BrowserID()
browserid.user_loader(get_user)
browserid.init_app(app)

from flask.ext.sslify import SSLify
sslify = SSLify(app)


