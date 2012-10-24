from matplotlib.pyplot import figure, show, xticks
import numpy as np
from math import pi
from random import randrange as rr 
fig = figure(figsize=(14,14))
labels = ["PC Team wellness", "Interdisciplinary Team", "Coverage/Ability",
        "Standard Form", "Initial PC evaluation", "Hospital PC screening",
        "PC follow up", "Post Discharge Services", "Bereavement Contacts",
        "Marking and Education","Marking and Education", "Care coordination",
        "Availability", "Family Centerdness", "PC Networking", 
        "Education and training", "Certification"]

ax = fig.add_subplot(111, polar=True)
deg = [360/len(labels) * x for x in range(1,len(labels)+1)]
radii = [i*pi/180 for i in deg]  # convert to radians

height = [rr(0,6) for x in range(len(labels))]
ax.bar(radii,height, width=0.2, align='center')

ax.set_thetagrids(deg,labels)

ax.set_title("like this Cheryl?", fontsize=20)
show()
