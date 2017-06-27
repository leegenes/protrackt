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

class Organization(Base):
    uuid = db.Column(db.String(32), db.ForeignKey('users.uuid'),
        nullable=False)
    name = db.Column(db.String(100),
        nullable=False)

    def __repr__(self):
        return self.name

class OrganizationDetail(Base):
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'),
        nullable=False)
    address1 = db.Column(db.String(75))
    address2 = db.Column(db.String(25))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(5))
    phone = db.Column(db.String(10))
    website = db.Column(db.String(100))



# exmaple for connecting tables
# class Polls(Base):
#     topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
#     option_id = db.Column(db.Integer, db.ForeignKey('options.id'))
#     vote_count = db.Column(db.Integer, default=0)
#     status = db.Column(db.Boolean)
#
#     topic = db.relationship('Topics', foreign_keys=[topic_id],
#             backref=db.backref('options', lazy='dynamic'))
#     option = db.relationship('Options', foreign_keys=[option_id])
#
#     def __repr__(self):
#         return self.option.name
