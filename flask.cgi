#!/usr/bin/env python
import cgitb
import os

cgitb.enable()  # Enable for debugging errors in the browser

# Ensure the SERVER_NAME is set
os.environ.setdefault('SERVER_NAME', 'i6.cims.nyu.edu')
os.environ.setdefault('SERVER_PORT', '443')
os.environ.setdefault('HTTPS', 'on')

from app import app
from wsgiref.handlers import CGIHandler

# Run the Flask app as a CGI application
CGIHandler().run(app)



