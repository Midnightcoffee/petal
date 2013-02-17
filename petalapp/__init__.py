'''
File: __init__.py
Date: 2013-02-16
Author: Drew Verlee
Description: load up the app, avoid import loops
'''

from flask import Flask, request
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

# Can't seem to separate out these into there own files
from flask.ext.admin.contrib.sqlamodel import ModelView
from petalapp.database.models import User, Organization, UserSurveySection,\
        SurveyHeader
from flask.ext.admin import BaseView, expose, Admin
from flask.ext.login import current_user
import datetime

#admin
class MyView(BaseView):


    @expose('/')
    def MyView(self):
        if request.method == 'POST':
            date_sumbitted = request.form['date_sumbitted']
            # YEAR MONTH DAY
            # datetime.date(*[int(x) for x in string_time.split('/')])

            for organization in Organization:
                uss = UserSurveySection(
                Organization.user_survey_sections.append(

        return self.render('MyView.html', current_user=current_user,
                SurveyHeader=SurveyHeader)

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.role == 2

class MyModelView(ModelView):

    @expose('/models/')
    def index(self):
        return self.render('index.html')

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.role == 2

admin = Admin(app, name='Gardner')
admin.add_view(MyView(name="Create a survey event"))
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Organization, db.session))
admin.add_view(MyModelView(UserSurveySection, db.session))
