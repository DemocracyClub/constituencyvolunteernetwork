#!/bin/bash

APPS="signup issue invite tasks tsc shorten"

for APP in "$APPS"
 do 
  echo "Testing $APP"
  ./manage.py test $APP
 done
