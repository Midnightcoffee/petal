'''
File: graph.py
Date: 2012-11-03
Author: Drew Verlee
Description: Contains function plotpolar
'''

import matplotlib.cm as cm
from matplotlib.pyplot import figure, gca, ylim
import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from random import randrange as rr
from math import pi
from petalapp.graphing_tools.labels import hospital_labels

#TODO: do something num and data..and this default, currently num
#serves only as a teaching method from how to extract a num from session
#TODO: re-factor out specific data
def plotpolar(data=[], num=None):
    """data and num used to build a graph using matplotlib,
       data[0]  is title
       data[1] is which_quarter
       data[2] is hospital_name
       data[3] is the list of radii
    """

    fig = figure(figsize=(10,10))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
    ax = gca()
    ax.set_autoscale_on(False)
    #xmin,xmax,ymin,ymax
    ylim(10)
    

    deg = [360/len(hospital_labels) * x for x in range(1,len(hospital_labels)+1)]
    theta = [i*pi/180 for i in deg]  # convert to radians
    #FIXME when possible reflect user input, atm random # of graph bars
    # random..
    if not data:
        radii = [rr(0,11) for x in range(len(hospital_labels)-1)]
        radii.append(num)
    else:
        title_ext = data[0] #leave blank for no title
        which_quarter = data[1]
        hospital_name = data[2]
        radii = data[3]

    #TODO creates graph bars
    bars = ax.bar(theta,radii, width=0.35, bottom=0.0, align='center')
    for r,bar in zip(radii, bars):
        bar.set_facecolor( cm.jet(r/10.))
        bar.set_alpha(0.5)

    #degree hospital_labels
    ax.set_thetagrids(deg,hospital_labels, frac= 1, fontsize=14, verticalalignment = 'top',weight ="bold", color = "blue",clip_on =True)
    #title
    ax.set_title(title_ext + " " + which_quarter + " " + hospital_name , fontsize=30, weight="bold")

    canvas=FigureCanvas(fig)
    #String.IO, i believe allows us to treat our object as if it were a file.
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)


    #how to return it to simple in views
    return png_output


