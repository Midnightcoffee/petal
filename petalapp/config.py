PORT = int(os.environ.get("PORT", 5000))
SECRET_KEY = str(os.environ.get("APP_SECRET_KEY"))
DEBUG = str(os.environ.get("DEBUG"))
SQLALCHEMY_DATABASE_URI=str(os.environ.get("DATABASE_URL"))
TESTING = os.environ.get("TESTING", False)
CSRF_ENABLED = True
