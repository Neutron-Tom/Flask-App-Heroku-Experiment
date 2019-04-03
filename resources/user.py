from flask_restful import Resource, reqparse
from models.user import UserModel
import sqlite3


class UserRegister(Resource):
    """Resource to handle user creation, called when a post
    request hits /register, as defined in app.py"""

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        required=True,
                        type=str,
                        help="Username is a required field")
    parser.add_argument('password',
                        required=True,
                        type=str,
                        help="Password is a required field")

    def post(self):
        data = UserRegister.parser.parse_args()

        # Check to see if user already exists
        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        # Not risky to directly use data for kwargs here, as its gone through parser
        user = UserModel(**data)

        user.save_to_db()

        return {'message': 'User created successfully'}, 201
