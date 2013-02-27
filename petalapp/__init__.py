'''
File: __init__.py
Date: 2013-02-16
Author: Drew Verlee
Description: load up the app, avoid import loops
'''

import datetime
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

from petalapp.flask_browserid.flaskext.browserid import BrowserID
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
from flask.ext.admin import BaseView, expose, Admin
from flask.ext.login import current_user
from petalapp.database.models import User, Organization, UserSurveySection,\
        SurveyHeader, Period, AssignedDue, Question, Answer, QuestionOption, Data

#admin
class ReturnToApp(BaseView):
    @expose('/')
    def return_to_app(self):
        return self.render('index.html')


class MyView(BaseView):

    @expose('/', methods=('GET','POST'))
    def MyView(self):
        # YEAR MONTH DAY
#TODO you need to add which organizations are allowed/have which survies.
#this is the reason for the m-to-m relationship, so that we can expose
# that different organizations have different survies. Below you just assigned
# all survey sections, ignoring this concept.

        survey_headers = None
        error = None
        if request.method == 'POST':
            survey_header_ids = [int(y) for y in request.form.getlist('survey_headers')]

            assigned = datetime.date(*[int(x) for x in
                request.form.get('assigned','0').split('/')])

            due = datetime.date(*[int(x) for x in
                request.form.get('due', '0').split('/')])

            start = datetime.date(*[int(x) for x in
                request.form.get('start', '0').split('/')])

            end = datetime.date(*[int(x) for x in
                request.form.get('end', '0').split('/')])

            name = request.form.get('name', None)

            p = Period(name=name, start=start, end=end)
            ad = AssignedDue(assigned=assigned, due=due)
            db.session.add(ad)
            db.session.add(p)
            for organization in Organization.query.all():

                for survey_header_id in survey_header_ids:
                    survey_header = SurveyHeader.query.get(survey_header_id)
                    if survey_header.name  == "Palliative Care Index": #FIXME
                        data = Data()
                        db.session.add(data)
                    for survey_sections in survey_header.survey_sections:
                        uss = UserSurveySection()
                        db.session.add(uss)
                        db.session.flush()
                        organization.user_survey_sections.append(uss)
                        survey_sections.user_survey_sections.append(uss)
                        p.user_survey_sections.append(uss)
                        ad.user_survey_sections.append(uss)
                        data.user_survey_sections.append(uss)

            db.session.commit()
            error =  "success"

        return self.render('MyView.html', current_user=current_user,
                SurveyHeader=SurveyHeader, survey_headers=survey_headers, error=error,
                Period=Period,AssignedDue=AssignedDue, UserSurveySection=UserSurveySection)

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.role == 2

class MyModelView(ModelView):

    @expose('/models/')
    def index(self):
        return self.render('index.html')

    def is_accessible(self):
        return current_user.is_authenticated() and current_user.role == 2

admin = Admin(app, name='Gardner')
admin.add_view(ReturnToApp(name='return to website'))
admin.add_view(MyView(name="Create a survey event"))
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Organization, db.session))
admin.add_view(MyModelView(UserSurveySection, db.session))
admin.add_view(MyModelView(Question, db.session))
admin.add_view(MyModelView(Answer, db.session))
admin.add_view(MyModelView(QuestionOption, db.session))
