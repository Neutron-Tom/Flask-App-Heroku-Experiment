from db import db

class StoreModel(db.Model):
    # SQLAlchemy table
    __tablename__ = 'stores'

    # SQLAlchemy column names
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180))

    # Create back-reference to the items in the store
    # This relies on SQLAlchemy finding a store_id in the
    # ItemModel
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        """Return a JSON representation of the model"""
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]} # How do we get self.items?

    @classmethod
    def find_by_name(cls, name):
        """Get item from the database.
        Defined here as a class method so that it can be used by the JWT
        authenticated 'get' as well as the non-authenticated 'post'"""

        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1

    def save_to_db(self):
        """Following SQLAlchemy code is good for both insert and update
        This is called 'upserting' apparently!"""

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    pass
