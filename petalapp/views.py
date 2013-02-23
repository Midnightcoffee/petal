'''
File: views.py
Date: 2012-11
Author: Drew Verlee
Description: contains the views for the webapp
'''

from sqlalchemy import func
from flask import render_template, url_for, redirect\
    , session, g, request, flash
from petalapp.database.models import User, Question, Answer , \
    Organization, SurveyHeader, SurveySection, SurveyComment, QuestionOption,\
    OptionChoice, OptionGroup,InputType,UserSurveySection, Period, AssignedDue,\
    ROLE_VIEWER, ROLE_ADMIN, ROLE_CONTRIBUTER, Data
from petalapp import db, app, lm
from flask.ext.login import current_user, login_required
from flask.ext.principal import Permission, RoleNeed, identity_loaded,\
    Identity, identity_changed, AnonymousIdentity

from aws_tools import upload_s3, get_url_s3
from graphing_tools.graph import plotpolar

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

@app.route("/")
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


from collections import namedtuple

SurveyTable = namedtuple('Survey_Table',['organization','organization_id','survey_header',
    'survey_section','survey_section_id','user_survey_section_id','completed','period_name',
    'period_start', 'period_end','assigned','due','questions'])

#TODO MOVE unpack
def unpack(user_survey_section_ids):
    survey_tables = []
    # new = [int(x) for x in user_survey_section_ids if not type(x) == int]

    for user_survey_section_id in user_survey_section_ids:
        if user_survey_section_id:
            uss = UserSurveySection.query.get(user_survey_section_id)
            organization = uss.organization.name
            organization_id = uss.organization.id
            ss_id = uss.survey_section.id
            ss = SurveySection.query.get(ss_id)
            ss_name = ss.name
            sh_name = ss.survey_header.name
            survey_header = sh_name
            if uss.completed_date:
                survey_section = ss_name
                completed = uss.completed_date.strftime("%Y-%d-%m")
            else:
                survey_section = uss.completed_date
                completed = uss.completed_date
            period_name = uss.period.name
            period_start = uss.period.start.strftime("%Y-%d-%m")
            period_end = uss.period.end.strftime("%Y-%d-%m")
            assigned = uss.assigned_due.assigned.strftime("%Y-%d-%m")
            due = uss.assigned_due.due.strftime("%Y-%d-%m")
            survey_table = SurveyTable(
                    organization=organization,
                    organization_id=organization_id,
                    survey_header=survey_header,
                    survey_section=survey_section,
                    survey_section_id=ss_id,
                    user_survey_section_id=user_survey_section_id,
                    period_name=period_name,
                    completed=completed,
                    period_start=period_start,
                    period_end=period_end,
                    assigned=assigned,
                    due=due,
                    questions=[]
                    )

            survey_tables.append(survey_table)
    return survey_tables



#TOD rename
@app.route('/super_survey',methods = ['GET', 'POST'])
@contributer_permission.require(403)
@login_required
def super_survey():
    #FIXME better way to see if survey?
    session['s3'] = None
    user_survey_section_ids = [x.user_survey_sections.order_by(UserSurveySection.completed_date.desc().
        nullslast()).first().id if x.user_survey_sections.order_by(UserSurveySection.completed_date.desc().
        nullslast()).first() else None for x in g.user.organizations]

    survey_tables = unpack(user_survey_section_ids)

    if  request.method == 'POST':
        session['user_survey_section_ids'] = []
        for survey_table in survey_tables:
            session['user_survey_section_ids'].append(request.form.
                    get(str(survey_table.user_survey_section_id)))

        if session['user_survey_section_ids']:
            return redirect(url_for('selection'))


    return render_template('super_survey.html',survey_tables=survey_tables,
            s3=session['s3']) #package=package)
#TODO bc primary keys start at 1 have questions start at 1 to.
#TODO move
#TODO were in UTC time switch it to local time
import datetime

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

    survey_tables = unpack(session['user_survey_section_ids'])
    if request.method == 'POST':
        for survey_table in survey_tables:
            data_section_total = 0
            question_ids = request.form.getlist(str(survey_table.survey_section_id))
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
            if user_survey_section.survey_section.order == 1:
                user_survey_section.data.standard_form = data_section_total


            data_values = extract_data(data)
            data_values = [int(x) for x in data_values] #TODO unicode
            #FIXME upload_s3 is calling plotpolar shouldn't
            #TODO refactor name groupings
            time = str(datetime.datetime.utcnow())
            upload_s3(survey_table.survey_header,
                    organization.name,
                    period.name,
                    time + ' ' + survey_table.survey_header
                    + ' ' + period.name + ' ' + organization.name ,
                    [survey_table.survey_header, period.name, organization.name, data_values])

            file_url =  get_url_s3('/'.join([survey_table.survey_header,
                organization.name, period.name, time + ' ' + survey_table.survey_header
                    + ' ' + period.name + ' ' + organization.name]))

            data.url = file_url
            db.session.commit()
            #TODO consider saving just 1




        session['user_survey_section_ids'] = None
        return redirect(url_for('super_survey'))

    return render_template('selection.html',survey_tables=survey_tables,
            SurveySection=SurveySection,user =g.user)
            # , user=g.user, id_packages=session['id_packages'],
            # SurveySection=SurveySection, Organization=Organization,User=User,
            # SurveyHeader=SurveyHeader)

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

# FIXME rename
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

#below are the views for various organizations
#TODO: possible move to their own file?
#TODO uncapitalized
@app.route("/MetroWest")
@login_required
@viewer_permission.require(403)
def MetroWest():
    return render_template("MetroWest.html")


@app.route("/st_vince")
@login_required
@viewer_permission.require(403)
def st_vince():
    return render_template("st_vince.html")


@app.route("/weiss_memorial")
@login_required
@viewer_permission.require(403)
def weiss_memorial():
    return render_template("weiss_memorial.html")


@app.route("/west_suburban")
@login_required
@viewer_permission.require(403)
def west_suburban():
    return render_template("west_suburban.html")


@app.route("/west_lake")
@login_required
@viewer_permission.require(403)
def west_lake():
    return render_template("west_lake.html")


@app.route("/childrens_organization_of_michigan")
@login_required
@viewer_permission.require(403)
def childrens_organization_of_michigan():
    return render_template("childrens_organization_of_michigan.html")


@app.route("/detroit_receiving")
@login_required
@viewer_permission.require(403)
def detroit_receiving():
    return render_template("detroit_receiving.html")


@app.route("/huron_valley_sinai")
@login_required
@viewer_permission.require(403)
def huron_valley_sinai():
    return render_template("huron_valley_sinai.html")


@app.route("/sinia_grace")
@login_required
@viewer_permission.require(403)
def sinia_grace():
    return render_template("sinia_grace.html")


@app.route("/harper_university")
@login_required
@viewer_permission.require(403)
def harper_university():
    return render_template("harper_university.html")


@app.route("/mac_neal")
@login_required
@viewer_permission.require(403)
def mac_neal():
    return render_template("mac_neal.html")


@app.route("/valley_baptist_harlingen")
@login_required
@viewer_permission.require(403)
def valley_baptist_harlingen():
    return render_template("valley_baptist_harlingen.html")


@app.route("/valley_baptist_brownsville")
@login_required
@viewer_permission.require(403)
def valley_baptist_brownsville():
    return render_template("valley_baptist_brownsville.html")


@app.route("/arizona_heart")
@login_required
@viewer_permission.require(403)
def arizona_heart():
    return render_template("arizona_heart.html")


@app.route("/arrow_head")
@login_required
@viewer_permission.require(403)
def arrow_head():
    return render_template("arrow_head.html")


@app.route("/maryvale")
@login_required
@viewer_permission.require(403)
def maryvale():
    return render_template("maryvale.html")


@app.route("/paradise_valley")
@login_required
@viewer_permission.require(403)
def paradise_valley():
    return render_template("paradise_valley.html")


@app.route("/phoenix_baptist")
@login_required
@viewer_permission.require(403)
def phoenix_baptist():
    return render_template("phoenix_baptist.html")


@app.route("/west_valley")
@login_required
@viewer_permission.require(403)
def west_valley():
    return render_template("west_valley.html")


@app.route("/st_lukes")
@login_required
@viewer_permission.require(403)
def st_lukes():
    return render_template("st_lukes.html")


@app.route("/northeast")
@login_required
@viewer_permission.require(403)
def northeast():
    return render_template("northeast.html")


@app.route("/north_central")
@login_required
@viewer_permission.require(403)
def north_central():
    return render_template("north_central.html")


@app.route("/mission_trail")
@login_required
@viewer_permission.require(403)
def mission_trail():
    return render_template("mission_trail.html")


