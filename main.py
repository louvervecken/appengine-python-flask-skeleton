""" main.py is the top level script.

Return "Hello World" at the root URL.
"""

import os
import sys

# sys.path includes 'server/lib' due to appengine_config.py
from flask import Flask
from flask import render_template
app = Flask(__name__.split('.')[0])

motion_enabled = False

@app.route('/')
def hello():
  """ Return hello template at application root URL."""
  return render_template('hello.html')

@app.route('/alarm-config')
def send_alarm_config():
	""" Return the current configuration the alarm needs to be put in. """
	return "motion_enabled = {0}".format(motion_enabled)
