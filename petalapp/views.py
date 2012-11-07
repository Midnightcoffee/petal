from flask import  make_response,render_template,url_for,request,redirect \
,session, flash
from petalapp import app
from flask.ext.wtf import FileField, Form
from tools import upload_s3_chart, download_s3_chart
from xtools import s3_upload
#python path points to petalapp?
from graph import plotpolar

#TODO add comments, doctrings?
#TODO change  main to base/welcome

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
    try:
        num = int(session['number'])
        assert (num >= 0 and num <= 10)
    except:
        num = 10
    response=make_response(plotpolar(num).getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route("/awspic")
def aws():
    destination_filename = 'achart'
    upload_s3_chart(5,destination_filename)
    k = download_s3_chart(destination_filename)
    return k.get_contents_to_filename("/".join([app.config["S3_UPLOAD_DIRECTORY"],destination_filename]))

class UploadForm(Form):
    example = FileField('Example File')

@app.route('/awswtf',methods=['POST','GET'])
def upload_page():
    form = UploadForm()
    if form.validate_on_submit():
        output = s3_upload(form.example)
        flash('{src} uploaded to S3 as {dst}'.format(src=form.example.data.filename, dst=output))
    return render_template('awswtf.html',form=form)



