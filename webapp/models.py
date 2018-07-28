from flask_sqlalchemy import SQLAlchemy
from webapp.extensions import bcrypt
from flask_login import AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app, g
# from extensions import auth

db = SQLAlchemy()

class Users(db.Model):
    # __tablename__ = 'user_table_name'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship(
        'Post', backref='user', lazy='dynamic'
    )

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<User `{}`>".format(self.username)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

Tags = db.Table('post_tags', db.Column('psot_id', db.Integer, db.ForeignKey('post.id')),
                db.Column('tag.id', db.Integer, db.ForeignKey('tag.id')))


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    comments = db.relationship(
        'Comment',
        backref='post',
        lazy='dynamic'
    )

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    tags = db.relationship('Tag',
                           secondary=Tags,
                           backref=db.backref('post', lazy='dynamic'))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Post '{}'>".format(self.title)


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])


class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)

    title = db.Column(db.String(255))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Tag '{}'>".format(self.title)