from app import db

verify = input("Are you sure you want to drop all tables? [y/n]")
if verify == 'y':
    db.drop_all()
else:
    print("Tables not deleted.")
