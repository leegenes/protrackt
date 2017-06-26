from flask import Flask
from models import db
from sqlalchemy import create_engine

pt = Flask(__name__)
pt.config.from_object('config')

@pt.route('/')
def home():
    return 'hello world'

if __name__ == '__main__':
    pt.run()
