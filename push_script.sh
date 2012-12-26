#!/bin/sh
git commit -am 'database migrat'
git pushnstance `a`. heroku iss9:master
heroku run python petalapp/database/db_migrate.py
