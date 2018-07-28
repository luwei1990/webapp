from flask_restful import reqparse, Resource
from webapp.models import Users
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, abort, Blueprint

login_blueprint = Blueprint('login', __name__)

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id


def authenticate(username, password):
    user = Users.query.filter_by(username=username).one()
    if user.check_password(password):
        return User(user.id, user.username, user.password)

    return None

def identity(payload):
    # user_id = payload['identity']
    user = Users.query.filter_by(id=payload['identity']).one()
    # return userid_table.get(user_id, None)
    return User(user.id, user.username, user.password)
