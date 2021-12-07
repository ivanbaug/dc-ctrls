import os
from dotenv import load_dotenv

# Loads environment variables from file
load_dotenv(".env")  # Comment after testing

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI")
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = os.environ.get("CSRF_KEY")

# Secret key for signing cookies
SECRET_KEY = os.environ.get("APP_KEY")

# Recaptcha config for site registration
RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUB_KEY")
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")
TESTING = False
