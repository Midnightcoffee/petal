'''
File: views.py
Date: 2012-11
Author: Drew Verlee
Description: contains the views for the webapp
'''
from flask import make_response, render_template, url_for, request, redirect\
    , session, redirect, g, flash
from petalapp.database.models import User, Hospital, Data, ROLE_USER, ROLE_ADMIN
from petalapp import db, app, lm, oid
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm
from petalapp.graphing_tools.graph import plotpolar

from petalapp.aws.tools import upload_s3
#python path points to petalapp?



@app.before_request
def before_request():
    '''run before every url request, to auth our user'''
    g.user = current_user

#post method possible to make awswtf work?
@app.route("/")
@app.route('/index')
def index():
    '''extends base and home of app ...'''
    user = g.user
    return render_template('index.html',user=user)


@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated() and g.user.email == 'drew.verlee@gmail.com':
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))



@app.route('/pci_form', methods = ['GET'])
@login_required
def pci_form():
    user = g.user
    return render_template('pci_form.html', user=user)


@app.route('/add_pci_form', methods = ['POST', 'GET'])
@login_required
def add_pci_form():
    test_hospital = Hospital('test_hospital')
    #TODO remove me
    db.session.add(test_hospital)
    db.session.commit()
    #TODO what if not integer
    test_data = Data(int(request.form['standard_form']),
                    int(request.form['marketing_education']),
                    int(request.form['record_availability']),
                    int(request.form['family_centerdness']),
                    int(request.form['pc_networking']),
                    int(request.form['education_and_training']),
                    int(request.form['team_funding']),
                    int(request.form['coverage']),
                    int(request.form['pc_for_expired_pts']),
                    int(request.form['hospital_pc_screening']),
                    int(request.form['pc_follow_up']),
                    int(request.form['post_discharge_services']),
                    int(request.form['certification']),
                    int(request.form['team_wellness']),
                    int(request.form['care_coordination'])
                    )
    db.session.add(test_data)
    db.session.commit()
    test_hospital.data.append(test_data)
    sample_data= Data.query.get(1)
    sample_hospital = Hospital.query.get(1)
    package = [str(sample_data.timestamp),'fake quarter', '100', [sample_data.standard_form, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    upload_s3('charts/quarter4'+ str(sample_data.timestamp)+ ' fake quarter ' + sample_hospital.name , package)

    return redirect(url_for('pci_form'))


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

#@app.route("/map")
#def map():
#    '''renders map of united states'''
#    return render_template('map.html')
#

#@app.route("/make_charts",methods=['GET','POST'])
#def make_charts():
#    '''helps make graphs/charts'''
#    if request.method == 'POST':
#        session['number'] = request.form['number']
#        return redirect(url_for('show_charts'))
#

#@app.route('/show_charts',methods= ['GET','POST'])
#def show_charts():
#    '''helps show graphs'''
#    #TODO should just copy this code ...
#    return render_template('show_charts.html')
#

#@app.route("/polarchart")
#def simple():
#    '''dynamically creates a chart'''
#    try:
#        num = int(session['number'])
#        assert (num >= 0 and num <= 10)
#    except:
#        num = 10
#    data = []
#    response=make_response(plotpolar(data, num).getvalue())
#    response.headers['Content-Type'] = 'image/png'
#    return response


#@app.route("/dbshow")
#def dbindex():
#    '''builds and shows a query from db'''
#    mydata = str(Hospital.query.all())
#    return render_template("dbshow.html",data=mydata)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/hospitals")
@login_required
def hospitals():
    '''page for hospitals'''
    return render_template("hospitals.html")

#below are the views for various hospitals
#TODO: possible move to their own file?
#TODO uncapitalized
@app.route("/MetroWest")
@login_required
def MetroWest():
    return render_template("MetroWest.html")


@app.route("/st_vince")
@login_required
def st_vince():
    return render_template("st_vince.html")


@app.route("/weiss_memorial")
@login_required
def weiss_memorial():
    return render_template("weiss_memorial.html")


@app.route("/west_suburban")
@login_required
def west_suburban():
    return render_template("west_suburban.html")


@app.route("/west_lake")
@login_required
def west_lake():
    return render_template("west_lake.html")


@app.route("/childrens_hospital_of_michigan")
@login_required
def childrens_hospital_of_michigan():
    return render_template("childrens_hospital_of_michigan.html")


@app.route("/detroit_receiving")
@login_required
def detroit_receiving():
    return render_template("detroit_receiving.html")


@app.route("/huron_valley_sinai")
@login_required
def huron_valley_sinai():
    return render_template("huron_valley_sinai.html")


@app.route("/sinia_grace")
@login_required
def sinia_grace():
    return render_template("sinia_grace.html")


@app.route("/harper_university")
@login_required
def harper_university():
    return render_template("harper_university.html")


@app.route("/mac_neal")
@login_required
def mac_neal():
    return render_template("mac_neal.html")


@app.route("/valley_baptist_harlingen")
@login_required
def valley_baptist_harlingen():
    return render_template("valley_baptist_harlingen.html")


@app.route("/valley_baptist_brownsville")
@login_required
def valley_baptist_brownsville():
    return render_template("valley_baptist_brownsville.html")


@app.route("/arizona_heart")
@login_required
def arizona_heart():
    return render_template("arizona_heart.html")


@app.route("/arrow_head")
@login_required
def arrow_head():
    return render_template("arrow_head.html")


@app.route("/maryvale")
@login_required
def maryvale():
    return render_template("maryvale.html")


@app.route("/paradise_valley")
@login_required
def paradise_valley():
    return render_template("paradise_valley.html")


@app.route("/phoenix_baptist")
@login_required
def phoenix_baptist():
    return render_template("phoenix_baptist.html")


@app.route("/west_valley")
@login_required
def west_valley():
    return render_template("west_valley.html")


@app.route("/st_lukes")
@login_required
def st_lukes():
    return render_template("st_lukes.html")


@app.route("/northeast")
@login_required
def northeast():
    return render_template("northeast.html")


@app.route("/north_central")
@login_required
def north_central():
    return render_template("north_central.html")


@app.route("/mission_trail")
@login_required
def mission_trail():
    return render_template("mission_trail.html")


