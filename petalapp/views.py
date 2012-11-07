from flask import  make_response,render_template,url_for,request,redirect \
,session, redirect
from petalapp import app
#from tools import upload_s3_chart, download_s3_chart
#python path points to petalapp?
from graph import plotpolar

#TODO add comments, doctrings?
#TODO change  main to base/welcome

#post method possible to make awswtf work?
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/map")
def map():
    #TODO fix up mainpage
    return render_template('map.html')

@app.route("/make_charts",methods=['GET','POST'])
def make_charts():
    if request.method == 'POST':
        session['number'] = request.form['number']
        return redirect(url_for('show_charts'))

@app.route('/show_charts',methods= ['GET','POST'])
def show_charts():
    #TODO should just copy this code ...
    return render_template('show_charts.html')


@app.route("/polarchart")
def simple():
    #TODO find out why there are imported in function, possible just import.
    #refactor this assert
    try:
        num = int(session['number'])
        assert (num >= 0 and num <= 10)
    except:
        num = 10
    response=make_response(plotpolar(num).getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/awsgraph", methods =['GET','POST'])
def aws():
    return render_template("awsgraph.html")




