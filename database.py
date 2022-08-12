'''
Module to store SQLLite db instance
'''
import os

from flask_sqlalchemy import SQLAlchemy

from config import SQL_DB_NAME, app

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, SQL_DB_NAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
