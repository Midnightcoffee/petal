from flask import Flask, make_response
app = Flask(__name__)

@app.route("/")
def simple():
    import datetime
    import StringIO
    import random

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response


if __name__ == "__main__":
    app.run()

# polar_bar.py
##!/usr/bin/env python
#
#import numpy as np
#import matplotlib.cm as cm
#from matplotlib.pyplot import figure, show, rc
#
#
## force square figure and square axes looks better for polar, IMO
#fig = figure(figsize=(8,8))
#ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
#
#N = 20
#theta = np.arange(0.0, 2*np.pi, 2*np.pi/N)
#radii = 10*np.random.rand(N)
#width = np.pi/4*np.random.rand(N)
#bars = ax.bar(theta, radii, width=width, bottom=0.0)
#for r,bar in zip(radii, bars):
#    bar.set_facecolor( cm.jet(r/10.))
#    bar.set_alpha(0.5)
#
#show()
