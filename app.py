"""This script launches the Flask server.

It has the functions having the Dash framework. These Dash functions are
bridged to the Flask Server, and they will
only render the Dash application when routed to the given paths

"""
from flask import Flask, render_template
from dash_models import dash_app_models

server = Flask(__name__)  # Flask server
# functions having the dash applications
dash_app_models(server, path='/models/')
# dash_app_countries(server, path='/countries/')


@server.route('/')  # home page renders the 'index.html'
def index():
    """Render index.html."""
    return render_template('index.html')


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080)
