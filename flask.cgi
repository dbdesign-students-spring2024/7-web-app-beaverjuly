
import os
import sys
sys.path.insert(0, '/misc/linux/centos7/x86_64/local/stow/python-3.6/lib/python3.6/site-packages/')

os.environ['REQUEST_METHOD'] = 'GET'

from wsgiref.handlers import CGIHandler
from app import app
CGIHandler().run(app)


