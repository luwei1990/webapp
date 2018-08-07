from flask_restful import reqparse, Resource
from webapp.models import Users
from flask import Blueprint
from webapp.models import db
from flask_jwt import jwt_required, current_identity

user_blueprint = Blueprint('user', __name__)


class UserService(Resource):
    def post(self):
        user_post = reqparse.RequestParser()
        user_post.add_argument('username', type=str, required=True)
        user_post.add_argument('password', type=str, required=True)
        args = user_post.parse_args()
        if Users.query.filter_by(username=args['username']).first() is not None:
            return {"msg":"user already exists"}, 401

        user = Users(username=args['username'])
        user.set_password(args['password'])
        db.session.add(user)
        db.session.commit()

    @jwt_required()
    def delete(self):
        user_del = reqparse.RequestParser()
        user_del.add_argument('username', type=str, required=True)
        # user_del.add_argument('token', type=str, required=True)
        args = user_del.parse_args()
        user = Users.query.filter_by(username=args['username']).one()
        db.session.delete(user)
        db.session.commit()

    @jwt_required()
    def put(self):
        user_del = reqparse.RequestParser()
        user_del.add_argument('username', type=str, required=True)
        args = user_del.parse_args()
        user = Users.query.filter_by(username=args['username']).one()
        Users.query.filter_by(username=args['username']).update({'password', user.set_password(args['password'])})
        db.session.commit()
