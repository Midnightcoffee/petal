#!flask/bin/python
from migrate.versioning import api
from petalapp.config import SQLALCHEMY_DATABASE_URI
from petalapp.config import SQLALCHEMY_MIGRATE_REPO
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print 'Current database version: ' + \
    str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))
