from flask import Flask
from flask_restful import Api

import env
from users import controller

# create instance of flask
app = Flask(__name__)

# create the API with app from flask_restful
api = Api(app)

api.add_resource(controller.UsersController, '/users')
app.run(host="0.0.0.0", port=3000, debug=True)
