import os
from flask import Flask, make_response,render_template,url_for,request,redirect,session,escape
app = Flask(__name__)

app.config.from_object('defaultconfig')
#app.config.from_envvar('PETAL_PRO')
#TODO doctrings?

@app.route("/")
def main():
    #TODO fix up mainpage
    return render_template('main.html')

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
    #TODO find out why there are imported in function
    import numpy as np
    import matplotlib.cm as cm
    from matplotlib.pyplot import figure, show, rc
    import datetime
    import StringIO
    import random
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter
    from random import randrange as rr
    from math import pi
    #TODO clean this up
    try:
        num = int(session['number'])
        assert num >= 0 and num <= 10
    except:
        num = 10
    
    labels = ["PC team wellness", "Interdisciplinary Team", "Coverage/Ability",
        "Standard Form", "Initial PC evaluation", "Hospital PC screening",
        "PC follow up", "Post Discharge Services", "Bereavement Contacts",
        "Marking and Education","Marking and Education", "Care coordination",
        "Availability", "Family Centerdness", "PC Networking",
        "Education and training", "Certification"]

    fig = figure(figsize=(12,12))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)


    deg = [360/len(labels) * x for x in range(1,len(labels)+1)]
    theta = [i*pi/180 for i in deg]  # convert to radians
    #FIXME for demo
    radii = [rr(0,11) for x in range(len(labels)-1)]
    radii.append(num)
    #TODO figure out width... artistically
    bars = ax.bar(theta,radii, width=0.35, bottom=0.0, align='center')
    for r,bar in zip(radii, bars):
        bar.set_facecolor( cm.jet(r/10.))
        bar.set_alpha(0.5)

    ax.set_thetagrids(deg,labels, frac= 1, fontsize=14, verticalalignment = 'top',weight ="bold", color = "blue",clip_on =True)

    ax.set_title("----PCI----", fontsize=30, weight="bold")

    canvas=FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
