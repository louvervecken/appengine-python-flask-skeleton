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
cpu_temp = 0.0
ram_perc = 0.0
free_storage = 0.0

@app.route('/')
def hello():
    """ Return hello template at application root URL."""
    return render_template('hello.html')

@app.route('/dashboard')
def dashboard():
    """ Show user dashboard. """
    return render_template('dashboard.html',
                           armed=alarm_enabled,
                           cpu_temp=cpu_temp,
                           ram_perc=ram_perc,
                           free_storage=free_storage)

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
        return redirect('/dashboard')
        
@app.route('/data-posting', methods=['POST'])
def post_data():
    """
    Receive data from rasp client to store in DB

    example on how to post from client side:
    import requests
    r = requests.post('https://rasp-lou-server.appspot.com/data-posting',
                      data={'cpu_temp': 44.3})
    """
    global cpu_temp, ram_perc, free_storage
    # if it is a post from the python client
    if request.method=='POST':
        cpu_temp = request.form.get('cpu_temp')
        ram_perc = request.form.get('ram_perc')
        free_storage = float(request.form.get('free_storage'))
        return "success", 201
