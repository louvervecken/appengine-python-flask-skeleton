""" main.py is the top level script.

Return "Hello World" at the root URL.
"""

import os
import sys

# sys.path includes 'server/lib' due to appengine_config.py
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
app = Flask(__name__.split('.')[0])

alarm_enabled = False

@app.route('/')
def hello():
    """ Return hello template at application root URL."""
    return render_template('hello.html')

@app.route('/alarm-config/dashboard')
def alarm_dashboard():
    """ Show user dashboard for alarm configuration and state. """
    return render_template('alarm-dashboard.html',
                           armed=alarm_enabled)

@app.route('/alarm-config/get')
def get_alarm_config():
    """ Return the current configuration the alarm needs to be put in. """
    return "alarm_enabled = {0}".format(alarm_enabled)

@app.route('/alarm-config/set', methods=['GET', 'POST'])
def set_alarm_config():
    """
    Config to set alarm on-or off.

    example on how to set on client side:
    import requests
    r = requests.post('https://rasp-lou-server.appspot.com/alarm-config/set',
                      data={'enabled': 'True'})
    """
    global alarm_enabled
    # if it is a post from the python client
    if request.method=='POST':
        alarm_enabled = request.form.get('enabled') == 'True'
        return "success", 201
    # or coming from dashboard
    else:
        alarm_enabled = request.args.get('enabled') == 'True'
        return redirect('/alarm-config/dashboard')