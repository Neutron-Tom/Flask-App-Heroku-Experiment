from db import db

class ItemModel(db.Model):
    # SQLAlchemy table
    __tablename__ = 'items'
    # SQLAlchemy column names
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180))
    price = db.Column(db.Float(precision=2))

    # Link items to a store. The item now has a property 'store'
    # which matches the store_id. This is a feature of SQLAlchemy
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        """Return a JSON representation of the model"""
        return {'name': self.name, 'price': self.price}

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
