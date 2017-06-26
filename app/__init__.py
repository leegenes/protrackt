from flask import Flask
from flask_sqlalchemy import SQLAlchemy

pt = Flask(__name__)
pt.config.from_object('config')
db = SQLAlchemy(pt)
