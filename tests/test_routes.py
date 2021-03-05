from app import app
from flask import session
from unittest import TestCase


app.config['TESTING'] = True

class TestRoutes(TestCase):

    