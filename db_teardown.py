from app import db

verify = input("are you sure you want to drop all tables? [y/n]")
if verify == 'y':
    db.drop_all()
