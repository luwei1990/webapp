# from flask_wtf import Form
# from wtforms import StringField, TextAreaField, PasswordField
# # from flask_wtf import Form, TextField, PasswordField, validators
#
# from wtforms.validators import DataRequired, Length
# import wtforms_json
# from models import User
# wtforms_json.init()
#
#
# class CommentForm(Form):
#     name = StringField(
#         'name',
#         validators=[DataRequired(), Length(max=255)]
#     )
#
#     text = TextAreaField('comment', validators=[DataRequired()])
#
#     def validate(self):
#         check_validate = super(CommentForm, self).validate()
#         if not check_validate:
#             return False
#
# class LoginForm(Form):
#     username = TextAreaField('username', [DataRequired()])
#     password = PasswordField('password', [DataRequired()])
#
#     def __init__(self, *args, **kwargs):
#         Form.__init__(self, *args, **kwargs)
#         self.user = None
#
#     def validate(self):
#         rv = Form.validate(self)
#         if not rv:
#             return False
#
#         user = User.query.filter_by(
#             username=self.username).first()
#         if user is None:
#             self.username.errors.append('Unknown username')
#             return False
#
#         if not user.check_password(self.password):
#             self.password.errors.append('Invalid password')
#             return False
#
#         self.user = user
#         return True
#
#
#

from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity

if __name__ == '__main__':
    app.run()



