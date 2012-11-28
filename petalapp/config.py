'''
File: config.py
Date: 2012-11
Author: Drew Verlee
Description: configuration setup to handle aws,heroku, local machine,
database, etc...
'''


import os

# flask
PORT = int(os.environ.get("PORT", 5000))
basedir = str(os.path.abspath(os.path.dirname(__file__)))
SECRET_KEY = str(os.environ.get("APP_SECRET_KEY"))
DEBUG = str(os.environ.get("DEBUG"))
ALLOWED_EXTENSIONS = str(os.environ.get("ALLOWED_EXTENSIONS"))
CSRF_ENABLED = True
TESTING = os.environ.get("TESTING", False)

#database, TODO add local db?
SQLALCHEMY_DATABASE_URI = str(os.environ.get("DATABASE_URL"))
SQLALCHEMY_MIGRATE_REPO = str(os.path.join(basedir, 'database/db_repository'))

# s3
AWS_ACCESS_KEY_ID = str(os.environ.get("AWS_ACCESS_KEY_ID"))
AWS_SECRET_ACCESS_KEY = str(os.environ.get("AWS_SECRET_ACCESS_KEY"))
S3_BUCKET = str(os.environ.get("S3_BUCKET"))
S3_UPLOAD_DIRECTORY = str(os.environ.get("S3_UPLOAD_DIRECTORY"))

