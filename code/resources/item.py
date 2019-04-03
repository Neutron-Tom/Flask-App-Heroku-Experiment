from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


# API works with resources, and resources are classes inherited from Resource
# Define a the resources. Presumably the decorators are added by Flask-Restful

class Item(Resource):
    """Manipulate individual items"""

    # Define this as a weird 'belongs to class but not a method'
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="Price is a required field")

    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="Every item must have a store id")

    # jwt_required decorator insists on the correct jwt token
    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {'message': 'An error occured accessing item from the database'}, 500

        if item:
            return item.json()
        return {'message': 'item not found'}, 404

    def post(self, name):  # Note that name comes via the URL, not JSON payload
        """Create a new item"""

        # First check to see if item already exists
        if ItemModel.find_by_name(name):
            return {"message": "an item with name {} already exists".format(name)}, 400

        # data = request.get_json() # Get JSON payload (errors if no/wrong payload)
        # data = request.get_json(force = True) # Don't look at the header, process even if incorrect
        # data = request.get_json(silent=True)  # Instead of raising an error, just returns none if issue with payload
        data = Item.parser.parse_args()

        # item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data) # Equivalent methods for unpacking dict as kwargs

        try:
            item.save_to_db()
            return item.json(), 201  # 201 is code for 'created'
        except:
            return {"message": "An error occurred inserting the item into the database"}, 500  # Internal server error

    def delete(self, name):
        """Delete the item from the list"""

        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}, 200

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            # Create an item
            # item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data)
            item.save_to_db()
            return item.json(), 201
        else:
            # Update item
            item.price = data['price']
            item.store_id = data['store_id']
            # Save changes to db
            # Flask-SQLAlchemy will actually create a new item if it doesn't exist, a benign diversion from the logic we'e set out here
            item.save_to_db()
            return item.json(), 200


class ItemList(Resource):
    """Get the list of all items"""

    def get(self):
        """Use SQLAlchemy query all to get entire table"""
        items = [item.json() for item in ItemModel.query.all()]
        return {'items': items}
