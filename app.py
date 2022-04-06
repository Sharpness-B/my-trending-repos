from library.github   import getCommits
from library.plotting import plotCommits

from flask import Flask, Response, request

import markdown
import markdown.extensions.fenced_code



app = Flask(__name__)



@app.route('/')
def home():
    readme_file = open("readme.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )

    md_css_string = "<style> pre { background: #f8f8f8; padding: 5px; width: fit-content; border-radius: 5px;} </style>"

    return md_css_string + md_template_string


@app.route('/<author>')
def chart(author):
    timespanDays = int( request.args.get('timespanDays') or 365 )
    setting      =      request.args.get('setting')      or "month"

    catalogue = getCommits(author, setting, timespanDays)
    bytes = plotCommits(catalogue, author, setting, timespanDays)

    return Response(bytes.getvalue(), mimetype="image/png")



if __name__ == '__main__':
    app.run()