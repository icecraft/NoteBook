#!/usr/bin/env python
# -*- coding: utf-8 -*
import os
from NoteBook import create_app
from NoteBook import db as notebook_db
from NoteBook.models import User, Note, Topic, Comment, Material
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

notebook = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(notebook)
migrate = Migrate(notebook, notebook_db)

def make_shell_context():
    return dict(app=app, notebook_db=notebook_db, User=User, Comment=Comment, Note=Note,\
                Topic=Topic, Material=Material )
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('notebook_db', MigrateCommand)



@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('NoteBook/tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def runtornado():
    http_server = HTTPServer(WSGIContainer(notebook))
    http_server.listen(5050)
    IOLoop.instance().start()

if __name__ == '__main__':
    import sys
    if sys.version_info.major < 3:
            reload(sys)
    sys.setdefaultencoding('utf8')
    manager.run()
