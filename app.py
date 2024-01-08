"""This script launches the Flask server.

It has the functions having the Dash framework. These Dash functions are
bridged to the Flask Server, and they will
only render the Dash application when routed to the given paths

"""
from datetime import datetime
from flask import Flask, render_template
from dash_models import dash_app_models

server = Flask(__name__)  # Flask server

# functions having the dash applications
dash_app_models(server, path='/models/')


@server.route('/')  # home page renders the 'index.html'
def index():
    """Render index.html."""
    today = datetime.today().year
    return render_template('index.html', year=today)


if __name__ == '__main__':
    server.run(port=5000)
