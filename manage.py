#!/usr/bin/env python
import os
from app.api_1_0.dbmanager import db,db_collection
from flask import current_app
from app.model import Contact

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app
from flask.ext.script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def drop_db():
    """Drop the database provided in the config"""
    db_name = current_app.config.get('MONGO_DB_NAME')
    db().connection.drop_database(db_name)

@manager.command
def populate_db():
    """Populate the database with some example values used from the config"""
    values = current_app.config.get('DB_EXAMPLE_VALUES')
    for phone,data in values:

        db_collection().insert({Contact.phone:phone,Contact.reg_id:data})


if __name__ == '__main__':
    manager.run()


