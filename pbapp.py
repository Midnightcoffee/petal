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
    


    # force square figure and square axes looks better for polar, IMO
    fig = figure(figsize=(8,8))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)

    N = 20
    theta = np.arange(0.0, 2*np.pi, 2*np.pi/N)
    radii = 10*np.random.rand(N)
    width = np.pi/4*np.random.rand(N)
    bars = ax.bar(theta, radii, width=width, bottom=0.0)
    for r,bar in zip(radii, bars):
        bar.set_facecolor( cm.jet(r/10.))
        bar.set_alpha(0.5) 
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
