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
    OptionChoice, OptionGroup,InputType, ROLE_VIEWER, ROLE_ADMIN, ROLE_CONTRIBUTER
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

#

@app.route('/organization',methods = ['GET', 'POST'])
@contributer_permission.require(403)
@login_required
def organization():
    error = None
    if request.method == 'POST':
        session['organization'] = request.form.get('organization',None)
        if not session['organization']:
            error = "Please select an organization"
        else:
            flash('Thank you')
            return redirect(url_for('survey_header'))
    return render_template('organization.html',
            organizations=g.user.organizations, error=error)

@app.route('/survey_header', methods = ['GET', 'POST'])
@contributer_permission.require(403)
@login_required
def survey_header():
    return render_template('survey_header.html')







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


