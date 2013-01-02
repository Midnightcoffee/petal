
import os
from flask import Flask
#alternative method
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from flask.ext.login import LoginManager
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, \
    MAIL_PASSWORD, SQLALCHEMY_DATABASE_URI
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
lm.init_app(app)
oid = OpenID(app, os.path.join(basedir, '/tmp'))


from petalapp.database import models
from petalapp import views


#note that we are only enabling the emails when we run without debugging.
#
#Testing this on a development PC that does not have an email server is easy,
#thanks to Python's SMTP debugging server. Just open a new console window
#(command prompt for Windows users) and run the following to start a fake email server:
#python -m smtpd -n -c DebuggingServer localhost:25
#
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT),
        'no-reply@' + MAIL_SERVER, ADMINS, 'microblog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/petal.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('petal startup')


