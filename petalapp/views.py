'''
File: views.py
Date: 2012-11
Author: Drew Verlee
Description: contains the views for the webapp
'''
from flask import make_response, render_template, url_for, request, redirect\
    , session, redirect, g, flash
#from petalapp.database.models import User, ROLE_USER, ROLE_ADMIN
from petalapp.database import models, db_temp
from petalapp import app, lm, oid
from forms import LoginForm
from graph import plotpolar

#from tools import upload_s3_chart, download_s3_chart
#python path points to petalapp?


#post method possible to make awswtf work?
@app.route("/")
def index():
    '''extends base and home of app ...'''
    user = { 'nickname': 'Drew' }
    return render_template('index.html',user=user)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])


@app.route("/map")
def map():
    '''renders map of united states'''
    return render_template('map.html')


@app.route("/make_charts",methods=['GET','POST'])
def make_charts():
    '''helps make graphs/charts'''
    if request.method == 'POST':
        session['number'] = request.form['number']
        return redirect(url_for('show_charts'))


@app.route('/show_charts',methods= ['GET','POST'])
def show_charts():
    '''helps show graphs'''
    #TODO should just copy this code ...
    return render_template('show_charts.html')


@app.route("/polarchart")
def simple():
    '''dynamically creates a chart'''
    try:
        num = int(session['number'])
        assert (num >= 0 and num <= 10)
    except:
        num = 10
    data = []
    response=make_response(plotpolar(data, num).getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


@app.route("/dbshow")
def dbindex():
    '''builds and shows a query from db'''
    mydata = str(models.Hospital.query.all())
    return render_template("dbshow.html",data=mydata)


@lm.user_loader
def load_user(id):
    return models.User.query.get(int(id))

@app.route("/hospitals")
def hospitals():
    '''page for hospitals'''
    return render_template("hospitals.html")

#below are the views for various hospitals
#TODO: possible move to their own file?
#TODO uncapitalized
@app.route("/MetroWest")
def MetroWest():
    return render_template("MetroWest.html")


@app.route("/st_vince")
def st_vince():
    return render_template("st_vince.html")


@app.route("/weiss_memorial")
def weiss_memorial():
    return render_template("weiss_memorial.html")


@app.route("/west_suburban")
def west_suburban():
    return render_template("west_suburban.html")


@app.route("/west_lake")
def west_lake():
    return render_template("west_lake.html")


@app.route("/childrens_hospital_of_michigan")
def childrens_hospital_of_michigan():
    return render_template("childrens_hospital_of_michigan.html")


@app.route("/detroit_receiving")
def detroit_receiving():
    return render_template("detroit_receiving.html")


@app.route("/huron_valley_sinai")
def huron_valley_sinai():
    return render_template("huron_valley_sinai.html")


@app.route("/sinia_grace")
def sinia_grace():
    return render_template("sinia_grace.html")


@app.route("/harper_university")
def harper_university():
    return render_template("harper_university.html")


@app.route("/mac_neal")
def mac_neal():
    return render_template("mac_neal.html")


@app.route("/valley_baptist_harlingen")
def valley_baptist_harlingen():
    return render_template("valley_baptist_harlingen.html")


@app.route("/valley_baptist_brownsville")
def valley_baptist_brownsville():
    return render_template("valley_baptist_brownsville.html")


@app.route("/arizona_heart")
def arizona_heart():
    return render_template("arizona_heart.html")


@app.route("/arrow_head")
def arrow_head():
    return render_template("arrow_head.html")


@app.route("/maryvale")
def maryvale():
    return render_template("maryvale.html")


@app.route("/paradise_valley")
def paradise_valley():
    return render_template("paradise_valley.html")


@app.route("/phoenix_baptist")
def phoenix_baptist():
    return render_template("phoenix_baptist.html")


@app.route("/west_valley")
def west_valley():
    return render_template("west_valley.html")


@app.route("/st_lukes")
def st_lukes():
    return render_template("st_lukes.html")


@app.route("/northeast")
def northeast():
    return render_template("northeast.html")


@app.route("/north_central")
def north_central():
    return render_template("north_central.html")


@app.route("/mission_trail")
def mission_trail():
    return render_template("mission_trail.html")


