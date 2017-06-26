from app import db
from app.models import Base, Users

db.create_all()

print("DB created.")
