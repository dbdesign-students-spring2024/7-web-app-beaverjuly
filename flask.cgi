#!/home/jy3813/public_html/7-web-app-beaverjuly/myenv/bin/python3
import sys
import os

# Add the directory containing your app to the Python path, if needed
sys.path.insert(0, '/home/jy3813/public_html/7-web-app-beaverjuly')

from wsgiref.handlers import CGIHandler
from app import app  # Make sure 'app' is the Flask instance

CGIHandler().run(app)


