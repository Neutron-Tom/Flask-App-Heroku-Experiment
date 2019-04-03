from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
# Turn off the FLASK SQLALCHEMY track modifications, not the one in actual SQLALCHEMY (ocnf
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Set the database location- this can be MySQL, Postgres, SQLITE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.secret_key = "rest python course"  # Strip this out of public code!
api = Api(app)  # From flask-restful

# Get SQLAlchemy to build tables in data.db for us
@app.before_first_request
def create_tables():
    db.create_all()

# Use the autheticate and identity functions we defined in 'security'
# JWT creates a new endpoint, /auth
# Data sent to /auth gets pushed to 'authenticate' function
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1/Item
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    # Import here to avoid a circular import
    from db import db
    db.init_app(app)

    app.run(port=5000, debug=True)
