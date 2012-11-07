import os

PORT = int(os.environ.get("PORT", 5000))
SECRET_KEY = str(os.environ.get("APP_SECRET_KEY"))
DEBUG = str(os.environ.get("DEBUG"))
SQLALCHEMY_DATABASE_URI=str(os.environ.get("DATABASE_URL"))
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
S3_BUCKET = os.environ.get("S3_BUCKET")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
TESTING = os.environ.get("TESTING", False)
S3_UPLOAD_DIRECTORY = os.environ.get("S3_UPLOAD_DIRECTORY")
ALLOWED_EXTENSIONS = os.environ.get("ALLOWED_EXTENSIONS")
CSRF_ENABLED = True
