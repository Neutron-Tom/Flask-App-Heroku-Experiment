import sqlite3
from db import db


class UserModel(db.Model):
    # Tell SQLAlchemy where this model will be stored
    __tablename__ = 'users'
    # Tell SQLAlchemy what columns the table contains
    # The id is added automatically by SQLAlchemy, even though it's not defined in the class
    id = db.Column(db.Integer, primary_key=True)  # N.B. shadowing the 'id' function here
    username = db.Column(db.String(180))  # Limited to 180 characters
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username  # Needs to be matched to the class-level property of type db.Column
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
