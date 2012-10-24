# polar_bar.py

import os
from flask import Flask, make_response
app = Flask(__name__)


@app.route("/")
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
    labels = ["PC team wellness", "Interdisciplinary Team", "Coverage/Ability",
        "Standard Form", "Initial PC evaluation", "Hospital PC screening",
        "PC follow up", "Post Discharge Services", "Bereavement Contacts",
        "Marking and Education","Marking and Education", "Care coordination",
        "Availability", "Family Centerdness", "PC Networking", 
        "Education and training", "Certification"]

    # force square figure and square axes looks better for polar, IMO
    fig = figure(figsize=(12,12))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)

    deg = [360/len(labels) * x for x in range(1,len(labels)+1)]
    theta = [i*pi/180 for i in deg]  # convert to radians

    radii = [rr(0,6) for x in range(len(labels))]
    #TODO figure out width... artistically
    bars = ax.bar(theta,radii, width=0.35, bottom=0.0, align='center')
    for r,bar in zip(radii, bars):
        bar.set_facecolor( cm.jet(r/10.))
        bar.set_alpha(0.5)
    
    ax.set_thetagrids(deg,labels, fontsize=15)

    ax.set_title("like this Cheryl?", fontsize=50, weight="bold")

    #TODO i'm assuming this is the paint part
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
