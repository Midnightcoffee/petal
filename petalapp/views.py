'''
File: views.py
Date: 2012-11
Author: Drew Verlee
Description: contains the views for the webapp
'''

from flask import render_template, url_for, redirect\
    , session, g, request, flash
from petalapp.database.models import User, Question, Answer , \
    Organization, SurveyHeader, SurveySection, SurveyComment, QuestionOption,\
    OptionChoice, OptionGroup,InputType,UserSurveySection, Period, AssignedDue,\
    ROLE_VIEWER, ROLE_ADMIN, ROLE_CONTRIBUTER
from petalapp import db, app, lm
from flask.ext.login import current_user, login_required
from flask.ext.principal import Permission, RoleNeed, identity_loaded,\
    Identity, identity_changed, AnonymousIdentity



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
        perm1 = Permission(RoleNeed(g.user.role))
        identity_changed.send(app, identity=Identity(g.user.role))
        session['logged_in'] = True
        rolelevel = g.user.role
        #TODO add some flashing
        #TODO consider maybe an add page... or something else?
    else:
        perm1 = Permission(RoleNeed(g.user)) # to represent no level aka Anonymou
        rolelevel = None
    return render_template('login.html', perm1=perm1,level=rolelevel)



@app.route('/logout')
def logout():
    identity_changed.send(app, Identity=AnonymousIdentity())
    session.pop('logged_in', None)
    return redirect(url_for("login")) #TODO should be something else?


# full page
from sqlalchemy import func
@app.route('/select_survey',methods = ['GET', 'POST'])
@contributer_permission.require(403)
@login_required
def select_survey():
    start_of_time = datetime.datetime(1,1,1)
    # max created survey section date
    if request.method == 'POST':
        unicode_ids = request.form.getlist('unicode_ids',None)
        if unicode_ids:
            #session['selection'] is [0:user.id, 1:org.id, 2:sh.id, 3:ss.id, 4:uss.id]
            session['id_packages'] = [[int(y) for y in x if y.isdigit()] for x in unicode_ids]

            return redirect(url_for('selection'))
    return render_template('select_survey.html',user=g.user,
            start_of_time=start_of_time)

from sqlalchemy import func
@app.route('/super_survey',methods = ['GET', 'POST'])
@contributer_permission.require(403)
@login_required
def super_survey():
    # org_id_mrs  = [db.session.query(UserSurveySection.id, func.max(
    #     UserSurveySection.completed_date)).filter_by(id=org.id).group_by(
    #         UserSurveySection).one() for org in g.user.organizations]
   db.session.query(UserSurveySection).order_by(UserSurveySection.completed_date.desc().nullslast()).first()
 

    #have [[uss id for most recent completed, most recent completed date]]
    # need: organization name for id, survey header name for id, period.name
    # period start period end, assigneddue.assigned, assigned due end
    # package = []
    # for uss_id_mr in org_id_mrs:
    #     y = {}
    #     uss = UserSurveySection.query.get(uss_id_mr[0])
    #     y['organization'] = uss.organization.name
    #     ss_id = uss.survey_section.id
    #     ss = SurveySection.query.get(ss_id)
    #     sh_name = ss.survey_header.name
    #     y['survey_header'] = sh_name
    #     y['survey_section'] = uss.completed_date.strftime("%Y-%d-%m")
    #     y['period_name'] = uss.period.name
    #     y['period_start'] = uss.period.start
    #     y['period_end'] = uss.period.end
    #     y['assigned_due.assigned'] = uss.assigned_due.assigned
    #     y['assigned_due.due'] = uss.assigned_due.due
    #     package.append(y)

    # .strftime("%Y-%d-%m")

    return render_template('super_survey.html',t=t) #package=package)
#TODO bc primary keys start at 1 have questions start at 1 to.
#TODO move
import datetime

@app.route('/selection',methods = ['GET', 'POST'])
@contributer_permission.require(403)
@login_required
def selection():
    question_ids = None
    if request.method == 'POST':
        if not session['id_packages']:
            return redirect(url_for('select_survey'))
        for id_package in session['id_packages']:
            question_ids = request.form.getlist('({0}, {1})'.format(
                id_package[3],id_package[4]))
            survey_section = SurveySection.query.get(id_package[3])
            user_survey_section = UserSurveySection.query.get(id_package[4])
            for question in survey_section.questions:
                if question.id in question_ids:
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

        db.session.commit()
        session['id_packages'] = None
        return redirect(url_for('select_survey'))

    return render_template('selection.html', user=g.user, id_packages=session['id_packages'],
            SurveySection=SurveySection, Organization=Organization,User=User,
            SurveyHeader=SurveyHeader)

@app.route('/organization',methods = ['GET', 'POST'])
@contributer_permission.require(403)
@login_required
def organization():
    error = None
    if request.method == 'POST':
            session['organization_id'] = request.form.get('organization_id',None)
            if session['organization_id']:
                return redirect(url_for('survey_header'))
            else:
                error = "Please select an organization"

    return render_template('organization.html',
            organizations=g.user.organizations, error=error)

@app.route('/survey_header', methods = ['GET', 'POST'])
@contributer_permission.require(403)
@login_required
def survey_header():
    if not session.get('organization_id', None):
        return redirect(url_for('organization'))
    else:
        error = None
        organization = Organization.query.get(session['organization_id'])
        if request.method == 'POST':
            session['survey_header_id'] = request.form.get('survey_header_id',None)
            session['time_period'] = request.form.get('user_survey_section_id',None)

            if session['survey_header_id']:
                return redirect(url_for('survey_section'))
            else:
                error = 'Please select a survey'
        return render_template('survey_header.html',
                Organization=Organization,
                organization_id=session['organization_id'],
                UserSurveySection=UserSurveySection,
                organization=organization,
                error=error)


@app.route('/survey_section', methods = ['GET', 'POST'])
@contributer_permission.require(403)
@login_required
def survey_section():
    #TODO maybe if not -> if
    if not (session.get('survey_header_id', None) and session.get('time_period',None)):
        return redirect(url_for('survey_header'))
    else:
        error = None
        if request.method == 'POST':
            session['survey_section_id'] = request.form.get('survey_section',None)
            if session['survey_header']:
                return redirect(url_for('question'))
            else:
                error = 'Please select a survey_section'
        return render_template('survey_section.html',
                Organization=Organization,
                SurveyHeader=SurveyHeader,
                organization_id=session['organization_id'],
                survey_header_id=session['survey_header_id'],
                error=error)


#
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


@app.route("/organizations")
@login_required
@contributer_permission.require(403)
def organizations():
    '''page for organizations'''
    return render_template("organizations.html")

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


