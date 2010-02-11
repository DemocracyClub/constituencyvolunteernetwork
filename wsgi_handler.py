#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
       
import django.core.handlers.wsgi

# Use this for application to find out which WSGI mode you are running in
#def application(environ, start_response):
#    status = '200 OK'
#
#    if not environ['mod_wsgi.process_group']:
#      output = 'EMBEDDED MODE'
#    else:
#      output = 'DAEMON MODE'
#
#    response_headers = [('Content-Type', 'text/plain'),
#                        ('Content-Length', str(len(output)))]
#
#    start_response(status, response_headers)
#
#    return [output]

application = django.core.handlers.wsgi.WSGIHandler()

