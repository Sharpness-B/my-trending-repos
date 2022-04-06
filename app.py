from flask import Flask, Response, request

from library.github import getCommits
from library.plotting import plotCommits



app = Flask(__name__)



@app.route('/')
def home():
    # https://dev.to/mrprofessor/rendering-markdown-from-flask-1l41
    return 'visit /your-github-username for your commit chart'



@app.route('/<author>')
def chart(author):
    timespanDays = int( request.args.get('timespanDays') or 365 )
    setting      =      request.args.get('setting')      or "month"

    catalogue = getCommits(author, setting, timespanDays)
    bytes = plotCommits(catalogue, author, setting, timespanDays)

    return Response(bytes.getvalue(), mimetype="image/png")



if __name__ == '__main__':
    app.run()