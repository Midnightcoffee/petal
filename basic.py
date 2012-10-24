from matplotlib.pyplot import figure, show
import matplotlib.cm as cm
from math import pi
from random import randrange as rr 
import numpy as np

labels = ["PC Team wellness", "Interdisciplinary Team", "Coverage/Ability",
        "Standard Form", "Initial PC evaluation", "Hospital PC screening",
        "PC follow up", "Post Discharge Services", "Bereavement Contacts",
        "Marking and Education","Marking and Education", "Care coordination",
        "Availability", "Family Centerdness", "PC Networking", 
        "Education and training", "Certification"]

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
show()
