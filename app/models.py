from app import db

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                                onupdate=db.func.current_timestamp())

class User(Base):
    username = db.Column(db.String(500))
    user_email = db.Column(db.String(75))
    user_password = db.Column(db.String(75))

    def __repr__(self):
        return self.username

class UserDetail(Base):
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_first = db.Column(db.String(50))
    user_last = db.Column(db.String(75))
    user_preferred = db.Column(db.String(50))

    def __repr__(self):
        return self.user_preferred

# TODO: build other table models with link to Users

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
