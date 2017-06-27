from app import db
from app.models import Base, Users, UserDetail, Organization, \
    OrganizationDetail

meta = db.metadata
tables = meta.sorted_tables
for t in tables:
    print(t)

verify = input('\n\ndo you want to delete the above tables and rebuild? [y/n]')
if verify =='y':
    db.drop_all()
    print('tables dropped')
    db.create_all()
    print('tables created')
    db.session.commit()
