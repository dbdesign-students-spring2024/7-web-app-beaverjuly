#!/usr/bin/env python3
import os
import sys

# Activate the virtual environment
activate_this = '/path/to/myenv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Now the environment's packages are available
sys.path.insert(0, '/misc/linux/centos7/x86_64/local/stow/python-3.6/lib/python3.6/site-packages/')
from wsgiref.handlers import CGIHandler
from app import app
CGIHandler().run(app)


