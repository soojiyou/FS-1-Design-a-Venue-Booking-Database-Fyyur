# from flask_script import Manager
from flask.cli import FlaskGroup
from flask_migrate import Migrate, MigrateCommand
from config import app
from flask_sqlalchemy import SQLAlchemy
from models import db


migrate = Migrate(app, db)
manager = FlaskGroup(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager()
