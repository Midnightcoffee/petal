'''
File: views.py
Date: 2012-11
Author: Drew Verlee
Description: contains the views for the webapp
'''
import datetime
from flask import render_template, url_for, redirect, session, g, request
from flask.ext.login import current_user, login_required
from flask.ext.principal import Permission, RoleNeed, identity_loaded,\
    Identity, identity_changed, AnonymousIdentity
from petalapp.database.models import User, Question, Answer , \
    Organization, SurveyHeader, SurveySection, SurveyComment, QuestionOption,\
    OptionChoice, OptionGroup,InputType,UserSurveySection, Period, AssignedDue,\
    ROLE_VIEWER, ROLE_ADMIN, ROLE_CONTRIBUTER, Data
from petalapp import db, app, lm
from aws_tools import upload_s3, get_url_s3
from petalapp.database.db_functions import unpack, most_recent_completed_uss
# permissions
viewer_permission = Permission(RoleNeed(ROLE_VIEWER))
contributer_permission = Permission(RoleNeed(ROLE_CONTRIBUTER))
admin_permission = Permission(RoleNeed(ROLE_ADMIN))




@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    """ identity.name is  g.user.role se for admin=2,contributer=1,viewer=0"""
    for roles in range(identity.name+1):
        identity.provides.add(RoleNeed(roles))


@app.before_request
def before_request():
    '''run before every url request, to auth our user'''
    g.user = current_user

#TODO bulid a proper homepage
@app.route('/')
def home():
    return render_template('home.html')






@app.route('/login', methods=['GET'])
def login():
    #TODO dont use g see tiny module
    if g.user.is_active():
        # perm1 = Permission(RoleNeed(g.user.role))
        identity_changed.send(app, identity=Identity(g.user.role))
        session['logged_in'] = True
        rolelevel = g.user.role
        #TODO add some flashing
        #TODO consider maybe an add page... or something else?
    else:
        # perm1 = Permission(RoleNeed(g.user)) # to represent no level aka Anonymou
        rolelevel = None
        #conider having a role level for anonymous
    if rolelevel:
        rolelevel = ['visitor','contributer', 'administrator'][rolelevel]
    return render_template('login.html', rolelevel=rolelevel, user=g.user)


@app.route('/logout')
def logout():
    identity_changed.send(app, Identity=AnonymousIdentity())
    session.pop('logged_in', None)
    return redirect(url_for("login")) #TODO should be something else?


#TOD rename
@app.route('/super_survey',methods = ['GET', 'POST'])
@contributer_permission.require(403)
@login_required
def super_survey():
    #FIXME better way to see if survey?
    # FIXME move function
    # user_survey_section_ids = [x.user_survey_sections.order_by(UserSurveySection.completed_date.desc().
    #     nullslast()).first().id if x.user_survey_sections.order_by(UserSurveySection.completed_date.desc().
    #     nullslast()).first() else None for x in g.user.organizations]
    user_survey_section_ids = most_recent_completed_uss(g.user)

    survey_tables = unpack(user_survey_section_ids)
    if  request.method == 'POST':
        session['user_survey_section_ids'] = []
        for survey_table in survey_tables:
            session['user_survey_section_ids'].append(request.form.
                    get(str(survey_table.user_survey_section_id)))
        if session['user_survey_section_ids']:
            return redirect(url_for('selection'))
    return render_template('super_survey.html',survey_tables=survey_tables,ids = user_survey_section_ids) #package=package)

#TODO bc primary keys start at 1 have questions start at 1 to.
#TODO move
#TODO were in UTC time switch it to local time
#FIXME move me
def extract_data(data):
    return [data.standard_form, data.marketing_education, data.record_availability,
    data.family_centerdness, data.pc_networking, data.education_and_training,
    data.team_funding, data.coverage, data.pc_for_expired_pts,
    data.hospital_pc_screening, data.pc_follow_up, data.post_discharge_services,
    data.bereavement_contacts, data.certification, data.team_wellness,
    data.care_coordination]


@app.route('/selection',methods = ['GET', 'POST'])
@contributer_permission.require(403)
@login_required
def selection():

    if not session.get('user_survey_section_ids',None):
        return redirect(url_for('super_survey'))

    # TODO rename survey_table
    # TODO move into own function
    survey_tables = unpack(session['user_survey_section_ids'])
    if request.method == 'POST':
        for survey_table in survey_tables:
            data_section_total = 0
            question_ids = request.form.getlist(str(survey_table.user_survey_section_id))
            survey_section = SurveySection.query.get(survey_table.survey_section_id)
            user_survey_section = UserSurveySection.query.get(survey_table.user_survey_section_id)
            data_id = user_survey_section.data.id
            data = Data.query.get(data_id)
            for question in survey_section.questions:
                if unicode(question.id) in question_ids: # because unicode
                    answer = Answer(tf=True)
                else:
                    answer = Answer(tf=False)
                option_choice = OptionChoice.query.filter_by(name='True').one()
                question_option = db.session.query(QuestionOption).\
                        filter((QuestionOption.question == question)
                                & (QuestionOption.option_choice == option_choice)).first()
                question_option.answers.append(answer)
                user_survey_section.answers.append(answer)
                user_survey_section.completed_date  = datetime.datetime.utcnow()
                organization = Organization.query.get(user_survey_section.organization.id)
                period = Period.query.get(user_survey_section.period.id)
                assigned_due = AssignedDue.query.get(user_survey_section.assigned_due.id)
                nuss = UserSurveySection()
                organization.user_survey_sections.append(nuss)
                survey_section.user_survey_sections.append(nuss)
                period.user_survey_sections.append(nuss)
                assigned_due.user_survey_sections.append(nuss)
                data.user_survey_sections.append(nuss)
                db.session.add(data) #TODO is this necessary?
                if answer.tf:
                    data_section_total += question_option.question.value
            #TODO generalize
            if user_survey_section.survey_section.order == 1:
                user_survey_section.data.standard_form = data_section_total
            elif user_survey_section.survey_section.order == 2:
                user_survey_section.data.marketing_education = data_section_total
            elif user_survey_section.survey_section.order == 3:
                user_survey_section.data.record_availability = data_section_total
            db.session.commit()
        # possible don't need this datas it was a commit problem.
            data_values = extract_data(data)
            data_values = [int(x) for x in data_values] #TODO unicode
            #FIXME upload_s3 is calling plotpolar shouldn't
            #TODO refactor name groupings
            time = str(datetime.datetime.utcnow())
            upload_s3(survey_table.survey_header,
                    survey_table.organization,
                    survey_table.period_name,
                    time + ' ' + survey_table.survey_header
                    + ' ' + survey_table.period_name + ' ' + survey_table.organization ,
                    [survey_table.survey_header, survey_table.period_name, survey_table.organization, data_values])
            file_url =  get_url_s3('/'.join([survey_table.survey_header,
                survey_table.organization, survey_table.period_name, time + ' ' + survey_table.survey_header
                    + ' ' + survey_table.period_name + ' ' + survey_table.organization]))
            data.url = file_url
            data.timestamp = time
            db.session.commit()
        #TODO consider saving just 1
        session['user_survey_section_ids'] = None
        return redirect(url_for('organization'))
    return render_template('selection.html',survey_tables=survey_tables,
            SurveySection=SurveySection,user =g.user)


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html')


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html')


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/organization", methods=['GET','POST'])
@login_required
@contributer_permission.require(403)
def organization():
    '''page for organizations'''
    session['organization_id'] = None
    if request.method == 'POST':
        session['organization_id'] = request.form.get('organization_id',None)
        #TODO check can i be on this page logic
        if session['organization_id']:
            return redirect(url_for('graph_view'))
    organizations = Organization.query.all()
    return render_template("organization.html",organizations=organizations)

#TODO rename
@app.route("/graph_view", methods=['GET','POST'])
@login_required
@contributer_permission.require(403)
def graph_view():
    data_c_url = db.session.query(Data).join(UserSurveySection).join(Organization).\
        filter(Organization.id==session['organization_id']).all()
    urls = [data.url for data in data_c_url]
    return render_template('graph_view.html', urls=urls)
