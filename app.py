from flask import Flask

import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from github import getCommits
from plotting import plotCommits

import json



app = Flask(__name__)



@app.route('/')
def home():
    # https://dev.to/mrprofessor/rendering-markdown-from-flask-1l41
    return 'visit /your-github-username for your commit chart'
  


@app.route('/<author>')
def chart(author):
    catalogue = getCommits(author)
    print(catalogue)
    return json.dumps( catalogue )
  


@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig



if __name__ == '__main__':
    app.run()