from app import pt
from app.models import db
from sqlalchemy import create_engine

@pt.route('/')
def home():
    return 'hello world'

if __name__ == '__main__':
    pt.run()
