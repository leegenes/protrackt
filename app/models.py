from app import db
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow,
                                onupdate=datetime.utcnow)

class Users(Base):
    uuid = db.Column(db.String(36),
        unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(50),
        unique=True, nullable=False)
    email = db.Column(db.String(75),
        unique=True, nullable=False)
    password = db.Column(db.String(75),
        unique=True, nullable=False)
    organizations = db.relationship('Organization', backref='users')

    def __repr__(self):
        return str(self.uuid) + ", " + self.username

class UserDetail(Base):
    uuid = db.Column(db.String(36), db.ForeignKey('users.uuid'),
        nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(75))
    preferred_name = db.Column(db.String(50))
    address1 = db.Column(db.String(75))
    address2 = db.Column(db.String(25))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(5))

    def __repr__(self):
        if not self.preferred_name:
            return self.first_name + ' ' + self.last_name
        return self.preferred_name + ' ' + self.last_name

class Experience(Base):
    __abstract__ = True
    @declared_attr
    def uuid(cls):
        return db.Column(db.String(36), db.ForeignKey('users.uuid'),
                nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    description = db.Column(db.Text)

class Organization(Experience):
    name = db.Column(db.String(75), nullable=False)
    address1 = db.Column(db.String(75))
    address2 = db.Column(db.String(25))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(5))
    phone = db.Column(db.String(10))
    website = db.Column(db.String(100))
    roles = db.relationship('Role', backref='organization')

# class Company(Organization):
#     roles = db.relationship('Role', backref='company')
#
# class School(Organization):
#     degrees = db.relationship('Degree', backref='school')

class Role(Experience):
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'),
        nullable=False)
    title = db.Column(db.String(50), nullable=False)
    # projects = db.relationship('Project', backref='role')

# class Degree(Experience):
#     name = db.Column(db.String(75), nullable=False)
#     has_degree = db.Column(db.Boolean, nullable=False)
#     courses = db.relationship('Course', backref='degree')
#
# class Course(Base):
#     degree_id = db.Column(db.Integer, db.ForeignKey('degree.id'),
#         nullable=False)
#     name = db.Column(db.String(50), nullable=False)
#     description = db.Column(db.Text)
#     projects = db.relationship('Project', backref='course')

class Project(Experience):
    name = db.Column(db.String(50), nullable=False)

class Skill(Base):
    name = db.Column(db.String(50), nullable=False, unique=True)

class ProjectSkill(Base):
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'),
        nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'),
        nullable=False)
