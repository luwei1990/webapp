from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
from flask_restful import Api
# from flask_httpauth import HTTPBasicAuth

bcrypt = Bcrypt()
# auth = HTTPBasicAuth()
# login_manager = LoginManager()
#
# login_manager.login_view = 'main.login'
# login_manager.session_protection = 'strong'
# login_manager.login_message = 'please login to acess this page'
# login_manager.login_message_category = 'info'

rest_api = Api()

# @login_manager.user_loader
# def load_user(userid):
#     from models import User
#     return User.query.get(userid)
