""" main.py is the top level script.

Return "Hello World" at the root URL.
"""

import os
import sys
import datetime

from google.appengine.ext import db
# sys.path includes 'server/lib' due to appengine_config.py
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
app = Flask(__name__.split('.')[0])

class StateAndSettings(db.Model):
    alarm_enabled = db.BooleanProperty(default=False, indexed=False)
    cpu_temp = db.FloatProperty(default=0.0, indexed=False)
    ram_perc = db.FloatProperty(default=0.0, indexed=False)
    free_storage = db.FloatProperty(default=0.0, indexed=False)

state_key = db.Key.from_path('StateAndSettings', 'state')
# create state if not yet existing
if not db.get(state_key):
    state = StateAndSettings(key_name='state')
    state.put()
else:
    state = db.get(state_key)
    
@app.route('/')
def hello():
    """ Return hello template at application root URL."""
    return render_template('hello.html')

@app.route('/dashboard')
def dashboard():
    """ Show user dashboard. """
    state = db.get(state_key)
    return render_template('dashboard.html',
                           armed=state.alarm_enabled,
                           cpu_temp=state.cpu_temp,
                           ram_perc=state.ram_perc,
                           free_storage=state.free_storage)

@app.route('/alarm-config/get')
def get_alarm_config():
    """ Return the current configuration the alarm needs to be put in. """
    state = db.get(state_key)
    return "alarm_enabled = {0}".format(state.alarm_enabled)

@app.route('/alarm-config/set', methods=['GET', 'POST'])
def set_alarm_config():
    """
    Config to set alarm on-or off.

    example on how to set on client side:
    import requests
    r = requests.post('https://rasp-lou-server.appspot.com/alarm-config/set',
                      data={'enabled': 'True'})
    """
    state = db.get(state_key)
    # if it is a post from the python client
    if request.method=='POST':
        state.alarm_enabled = request.form.get('enabled') == 'True'
        state.put()
        return "success", 201
    # or coming from dashboard
    else:
        state.alarm_enabled = request.args.get('enabled') == 'True'
        state.put()
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
    state = db.get(state_key)
    # if it is a post from the python client
    if request.method=='POST':
        state.cpu_temp = request.form.get('cpu_temp')
        state.ram_perc = request.form.get('ram_perc')
        state.free_storage = float(request.form.get('free_storage'))
        state.put()
        return "success", 201
