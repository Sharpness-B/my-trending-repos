from flask import Flask, Response

from github import getCommits
from plotting import plotCommits



app = Flask(__name__)



@app.route('/')
def home():
    # https://dev.to/mrprofessor/rendering-markdown-from-flask-1l41
    return 'visit /your-github-username for your commit chart'



@app.route('/<author>')
def chart(author):
    catalogue = getCommits(author)
    bytes = plotCommits(catalogue, 365, "month", author)

    return Response(bytes.getvalue(), mimetype="image/png")



if __name__ == '__main__':
    app.run()