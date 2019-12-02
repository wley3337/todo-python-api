from flask import Flask
from flask_restful import Api

import env
from users import users_controller, create_user_account
from login import login

# create instance of flask
app = Flask(__name__)

# create the API with app from flask_restful
api = Api(app)


# Routes need to be defined before server spins up
api.add_resource(create_user_account.CreateUserAccount, '/create-user')
api.add_resource(login.Login, '/login')

api.add_resource(users_controller.UsersAutoLogin, '/users/show')
api.add_resource(users_controller.UsersController, '/users')


app.run(host="0.0.0.0", port=3000, debug=True)
