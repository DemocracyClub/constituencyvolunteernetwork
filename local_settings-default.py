# Local settings file for Democracy Club website

# Debug settings
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Database settings
DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'volnet'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Email settings
DEFAULT_FROM_EMAIL = "democracyclub@localhost"

# If you have a local SMTP server with no authentication for local connections
EMAIL_HOST = "localhost"

# If you want to use GMail's SMTP server
#EMAIL_HOST = "smtp.gmail.com"
#EMAIL_HOST_USER = "you@gmail.com"
#EMAIL_HOST_PASSWORD = "your_password"
#EMAIL_USE_TLS = True
#EMAIL_PORT = 587

# Setting this to blank disables GA tracking
GOOGLE_ANALYTICS_ID = ""
