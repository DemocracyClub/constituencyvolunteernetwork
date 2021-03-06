# Django settings for fryweb project.
import os
PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Seb Bacon', 'seb.bacon@gmail.com'),
)

MANAGERS = ADMINS
DEFAULT_FROM_EMAIL = 'no-reply@democracyclub.org.uk'
DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'volnet'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, "media/")


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/resources/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'nsryqx^q8*0$2f8vdwm^_e0bawp=_c5(&$maleaix^exjzvain'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
#    'reversion.middleware.RevisionMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates"),
    os.path.join(PROJECT_PATH, "casestudies", "templates"),
    
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "context_processors.navigation",
    "context_processors.current_site",
    "context_processors.google_analytics",
    "context_processors.is_debug",
)

INSTALLED_APPS = (
    'south',
    'reversion',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'tasks', # note: 'tasks' must be first app (due to Proxy models)
    'django.contrib.comments',
    'comments_custom',
    'signup',
    'invite',
    'issue',
    'tsc',
    'shorten',
    'meetings',
    'ynmp',
    'twfy'
)

AUTHENTICATION_BACKENDS = ('backends.NoAuthBackend',
                           'django.contrib.auth.backends.ModelBackend',
                           )
MIGRATIONS_ROOT = os.path.join(PROJECT_PATH, 'migrations')

LOGIN_URL = "/?notice=You%20must%20be%20logged%20in%20to%20view%20that%20page.%20Sign%20up%20below%20to%20get%20started,%20or%20If%20you%20did%20log%20in,%20check%20your%20cookie%20settings.&"

COMMENTS_APP = "comments_custom"                           

import datetime
CONSTITUENCY_YEAR = datetime.datetime(2010, 1, 1)

ACCOUNT_ACTIVATION_DAYS = 40

GOOGLE_ANALYTICS_ID = "UA-10926972-1"

SOUTH_AUTO_FREEZE_APP = True

CACHE_MIDDLEWARE_SECONDS = 60 * 60 
CACHE_MIDDLEWARE_KEY_PREFIX = ""
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_BACKEND = "memcached://127.0.0.1:11211/"

YNMP_URL = "http://stage.yournextmp.com/"
YNMP_SECRET_KEY = "SECRET_KEY"
TWFY_SECRET_KEY = ""

try:
    from local_settings import *
except ImportError:
    pass
