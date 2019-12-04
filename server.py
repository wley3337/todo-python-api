from flask import Flask
from flask_restful import Api

# Load ENV variables
from config import env

from users import users_controller, create_user_account
from login import login
from to_dos import to_dos_controller
from lists import lists_controller


# create instance of flask
app = Flask(__name__)

# create the API with app from flask_restful
api = Api(app)

# Routes need to be defined before server spins up
# Open Routes
api.add_resource(create_user_account.CreateUserAccount, '/create-user')
api.add_resource(login.Login, '/login')

# JWT Protected Routes
api.add_resource(users_controller.UsersAutoLogin, '/users/show')
api.add_resource(users_controller.UsersController, '/users')
api.add_resource(lists_controller.ListsController, '/lists')
api.add_resource(to_dos_controller.ToDos, '/to-dos')

# Start server
app.run(host="0.0.0.0", port=3000, debug=True)


# Decorratior pattern for auth Routes
# def auth_wrapper(func):
#   def auth():
#     if 1 + 1 == 2:
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
