from flask import Blueprint, abort
from flask_restful import Resource, Api, reqparse


from webapp.models import db, Post, Tag, Comment, Users, Tags
from flask_jwt import jwt_required, current_identity

blog_blueprint = Blueprint('blog', __name__)


class BlogService(Resource):
    @jwt_required()
    def post(self):
        data = reqparse.RequestParser()
        data.add_argument('title', type=str, required=True)
        data.add_argument('text', type=str, required=True)
        args = data.parse_args()

        post = Post(args['title'])
        post.text = args['text']
        db.session.add(post)
        db.session.commit()

    def get(self):
        data = reqparse.RequestParser()
        data.add_argument('title', type=str, required=True)
        args = data.parse_args()
        post = Post.query.filter_by(title=args['title']).one()
        return {'title': post.title, 'text': post.text}

    @jwt_required()
    def put(self):
        pass

    @jwt_required()
    def delete(self):
        data = reqparse.RequestParser()
        data.add_argument('title', type=str, required=True)
        args = data.parse_args()
        post = Post.query.filter_by(title=args['title']).one()
        db.session.delete(post)
        db.session.commit()



