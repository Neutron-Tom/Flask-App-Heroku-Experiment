from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    """Stores contain items"""

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': 'Store not found'}, 404

    def post(self, name):
        """ Check if store exists, if not create it"""
        if StoreModel.find_by_name(name):
            return {'message': 'A store called {} already exists'.format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred creating the store.'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}, 200


class StoreList(Resource):
    """List all stores"""

    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
