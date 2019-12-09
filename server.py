from flask import Flask
from flask_restful import Api
from flask_cors import CORS

# Load ENV variables
import config.env

from users.users_controller import UsersController, UsersAutoLogin
from users.create_user_account import CreateUserAccount
from login.login import Login
from to_dos.to_dos_controller import ToDosController
from lists.lists_controller import ListsController
from util.jwt_handler import auth_decorator


# create instance of flask
app = Flask(__name__)
# CORS(app, support_credentials=True)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# create the API with app from flask_restful
api = Api(app)

# Routes need to be defined before server spins up
# Open Routes
api.add_resource(CreateUserAccount, '/create-user')
api.add_resource(Login, '/login')

# JWT Protected Routes
# @auth_decorator
api.add_resource(UsersAutoLogin, '/users/show')

api.add_resource(UsersController, '/users')
api.add_resource(ListsController, '/lists',  '/lists/<int:list_id>')
api.add_resource(ToDosController, '/to-dos', '/to-dos/<int:to_do_id>')

# Start server
app.run(host="0.0.0.0", port=3000, debug=True)


# Decorator pattern for auth Routes
# def auth_wrapper(func):
#   def auth():
#     if 1 + 2 == 2:
#       func()
#       return "authorized"
#     else:
#       print("not authorized")
#       return "this is returned"
#   return auth


# @auth_wrapper
# def this():
#   print("this should not print.")


# print(this())
