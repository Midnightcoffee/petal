import os
#TODO: add str? to everything?

PORT = int(os.environ.get("PORT", 5000))
basedir = str(os.path.abspath(os.path.dirname(__file__)))
SECRET_KEY = str(os.environ.get("APP_SECRET_KEY"))
DEBUG = str(os.environ.get("DEBUG"))
SQLALCHEMY_DATABASE_URI=str(os.environ.get("DATABASE_URL"))
AWS_ACCESS_KEY_ID = str(os.environ.get("AWS_ACCESS_KEY_ID"))
S3_BUCKET = str(os.environ.get("S3_BUCKET"))
AWS_SECRET_ACCESS_KEY = str(os.environ.get("AWS_SECRET_ACCESS_KEY"))
TESTING = os.environ.get("TESTING", False)
S3_UPLOAD_DIRECTORY = str(os.environ.get("S3_UPLOAD_DIRECTORY"))
ALLOWED_EXTENSIONS = str(os.environ.get("ALLOWED_EXTENSIONS"))
CSRF_ENABLED = True
SQLALCHEMY_MIGRATE_REPO = str(os.path.join(basedir, 'db_repository'))
