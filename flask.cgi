#!/usr/bin/env python3
import os
import sys

# Activate the virtual environment
activate_this = '/home/jy3813/public_html/7-web-app-beaverjuly/myenv/bin/app.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Adjust the path to where the Python packages are installed within the virtual environment
sys.path.insert(0, '/home/jy3813/public_html/7-web-app-beaverjuly/myenv/lib/python3.6/site-packages/')
from wsgiref.handlers import CGIHandler
from app import app
CGIHandler().run(app)

