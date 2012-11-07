'''
File: graph.py
Date: 2012-11-03
Author: Drew Verlee
Description: Contains function plotpolar
'''

import matplotlib.cm as cm
from matplotlib.pyplot import figure
import StringIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from random import randrange as rr
from math import pi

def plotpolar(num):
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
    #FIXME when possible reflect user input, atm random # of graph bars
    radii = [rr(0,11) for x in range(len(labels)-1)]
    radii.append(num)
    #TODO creates graph bars
    bars = ax.bar(theta,radii, width=0.35, bottom=0.0, align='center')
    for r,bar in zip(radii, bars):
        bar.set_facecolor( cm.jet(r/10.))
        bar.set_alpha(0.5)

    #degree labels
    ax.set_thetagrids(deg,labels, frac= 1, fontsize=14, verticalalignment = 'top',weight ="bold", color = "blue",clip_on =True)
    #title
    ax.set_title("----PCI----", fontsize=30, weight="bold")

    canvas=FigureCanvas(fig)
    #String.IO, i believe allows us to treat our object as if it were a file.
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    return png_output



