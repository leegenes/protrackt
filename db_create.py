from app import db
from app.models import Base, User

db.create_all()

print("DB created.")
