'''
File: test.py
Date: 2012-12-06
Author: Drew Verlee
Description: tests for petal
'''
from flask.ext.testing import TestCase

from myapp import create_app, db

class MyTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite://test.db"
    TESTING = True

    def create_app(self):

        # pass in test configuration
        return create_app(self)

    def setUp(self):

        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()
