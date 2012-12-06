#!/bin/sh
git add .
git commit -m 'shell script push'
git push heroku iss8:master
heroku run python petalapp/database/db_migrate.py
heroku run python petalapp/database/db_test_many_create.py
