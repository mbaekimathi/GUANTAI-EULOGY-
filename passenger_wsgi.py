"""
cPanel / Phusion Passenger entry point.
Setup Python App: startup file passenger_wsgi.py, entry point application.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from config.wsgi import application
