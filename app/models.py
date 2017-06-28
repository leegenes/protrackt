# TODO: resolve foreign key conflicts with uuid
# TODO: write projects model; uncomment relationships to it

from app import db

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                                onupdate=db.func.current_timestamp())

class Users(Base):
    uuid = db.Column(db.String(32),
        unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(50),
        unique=True, nullable=False)
    email = db.Column(db.String(75),
        unique=True, nullable=False)
    password = db.Column(db.String(75),
        unique=True, nullable=False)
    companies = db.relationship('Company', backref='users')
    schools = db.relationship('School', backref='users')

    def __repr__(self):
        return str(self.uuid) + ", " + self.username

class UserDetail(Base):
    uuid = db.Column(db.String(32), db.ForeignKey('users.uuid'),
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
    uuid = db.Column(db.String(32), db.ForeignKey('users.id'),
            nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    description = db.Column(db.Text)

class Organization(Experience):
    __abstract__ = True

    name = db.Column(db.String(50), unique=True, nullable=False)
    address1 = db.Column(db.String(75))
    address2 = db.Column(db.String(25))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(5))
    phone = db.Column(db.String(10))
    website = db.Column(db.String(100))

class Company(Organization):
    uuid = db.Column(db.String(32), db.ForeignKey('users.id'),
        nullable=False)
    roles = db.relationship('Role', backref='company')

class Role(Experience):
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'),
        nullable=False)
    title = db.Column(db.String(50), nullable=False)
    # projects = db.relationship('Project', backref='role')

class School(Organization):
    uuid = db.Column(db.String(32), db.ForeignKey('users.id'),
        nullable=False)
    focuses = db.relationship('Focus', backref='school')

class Focus(Experience):
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'),
        nullable=False)
    title = db.Column(db.String(50), nullable=False)
    has_degree = db.Column(db.Boolean, nullable=False)
    # projects = db.relationship('Project', backref='focus')

class Course(Base):
    focus_id = db.Column(db.Integer, db.ForeignKey('focus.id'),
        nullable=False)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    # projects = db.relationship('Project', backref='course')
