from models.user import UserModel
from werkzeug.security import safe_str_cmp


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    # Use Werkzeug safe string comparison tool to protect against ASCII/UNICODE differences
    if user and safe_str_cmp(user.password, password):
        return user


# This identity function is unique to the flask-jwt library we just imported
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)

