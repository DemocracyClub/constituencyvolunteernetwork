Note: if you need help, you might find some of us on the `#democracyclub` channel on `freenode`

# Python modules #

You'll need to install:
  * Either Python 2.5 or Python 2.6.
  * If you're using Python 2.5, [simplejson](http://pypi.python.org/pypi/simplejson) (Debian package python-simplejson)
  * If you're using PostgreSQL, psycopg2 (Debian package python-psycopg2)
  * South 0.6.2 (or above) (Debian package python-django-south - NB: I had issues with the Ubuntu South package and had to install it manually from [the website](http://south.aeracode.org/). Do not install the package via apt for now, it appears to be broken.)
  * Django 1.1

# Setting up the sandbox #

  * Download the site code
  * Copy local\_settings-default.py to local\_settings.py. If you don't run your own local email server, there is an example for making it use GMail.
  * Create a PostgreSQL database, or set up your own database configuration in local\_settings.py
  * Run `./manage.py test` to see if everything works
  * Run `./manage.py syncdb; ./manage.py migrate signup; ./manage.py migrate` to get your tables set up for a dev database
  * Run `./manage.py constituencies load` to populate the db with constituency data
  * Run `./manage.py loaddata test_tasks.json` to populate the db with some tasks
  * Run `./manage.py loadynmp --file=/tmp/yournextmp.json` to populate the db with data from YourNextMP (will need to download the JSON file from there first)
  * To update the heatmap PNG, you'll want to run something like `wget -O - http://www.democracyclub.org.uk/statistics/heatmap.svg | rsvg-convert -a -w 400 > media/images/heatmap.png` as a cron job

# Code overview #

The code is split into the following Django applications:

  * **signup** - Handles signup, constituency allocation and the front page
  * **tasks** - Task framework, handles member task assignment and UI
  * **comments\_custom** - Comments framework, modifies the default Django comments framework by stripping out un-necessary fields.
  * **shorten** - URL shortening framework. Takes urls and spits out shortened urls, and then redirects the short urls to the given URL

These applications relate to specific tasks:

  * **invite** - Allows a user to invite other people, sample task
  * **issue** - Issue application for the issue gathering task
  * **tsc** - The Straight Choice application for the TSC leaflet gathering task