from webapp.config import DevConfig
from flask import Flask
from flask_jwt import JWT
from .controllers.login import authenticate, identity

from models import db, Users

from controllers.blog import blog_blueprint
from controllers.user import user_blueprint
from controllers.login import login_blueprint
from webapp.extensions import bcrypt, rest_api
from .controllers.user import UserService
from .controllers.blog import BlogService


app = Flask(__name__)

app.config.from_object(DevConfig)
app.config['SECRET_KEY'] = 'super-secret'
db.init_app(app)
bcrypt.init_app(app)
jwt = JWT(app, authenticate, identity)


app.register_blueprint(user_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(blog_blueprint)

rest_api.add_resource(UserService, '/user')
rest_api.add_resource(BlogService, '/blog')
rest_api.init_app(app)


# @auth.verify_password
# def verify_password(username_or_token, password):
#     # first try to authenticate by token
#     user = User.verify_auth_token(username_or_token)
#     if not user:
#         # try to authenticate with username/password
#         user = User.query.filter_by(username=username_or_token).first()
#         if not user or not user.check_password(password):
#             return False
#     # g.user = user
#     return True


# @app.before_request
# def before_request():
#     # print request.cookies
#     # session['user_id'] = request.cookies['session']
#     user = User.query.get(session.get('user_id'))
#     if not user:
#         username = request.json['username']
#         password = request.json['password']
#         user = User.query.filter_by(username=username, password=password).first()
#         session['user_id'] = user.id
#
#     if 'user_id' in session:
#         g.user = User.query.get(session['user_id'])
#     else:
#         g.user = None
from tasks import add

@app.route('/')
def index():
    result = add.apply_async(args=[40, 69])
    print result
    return str(result.get())


@app.route('/status/<task_id>')
def get_status(task_id):
    result = add.AsyncResult(task_id)
    return result.state




