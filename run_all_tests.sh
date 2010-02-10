#!/bin/bash

APPS="signup issue invite tasks"

for APP in "$APPS"
 do 
  echo "Testing $APP"
  ./manage.py test $APP
 done
