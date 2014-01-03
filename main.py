""" main.py is the top level script.

Return "Hello World" at the root URL.
"""

import os
import sys

# sys.path includes 'server/lib' due to appengine_config.py
from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__.split('.')[0])

motion_enabled = False
temp_var = "bla"

@app.route('/')
def hello():
    """ Return hello template at application root URL."""
    return render_template('hello.html')

@app.route('/alarm-config/get-motion')
def get_motion_config():
    """ Return the current configuration the alarm needs to be put in. """
    return "motion_enabled = {0}".format(motion_enabled)

@app.route('/alarm-config/get-test')
def get_test():
    """ Return the current configuration the alarm needs to be put in. """
    return temp_var

@app.route('/alarm-config/set-motion', methods=['POST'])
def set_motion_config():
    global temp_var
    temp_var = str(request.values)
    return "success", 201