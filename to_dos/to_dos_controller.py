from flask_restful import Resource
from to_dos import to_dos_model
from util.jwt_handler import auth_decorator


class ToDosController(Resource):
    method_decorators = [auth_decorator]

    def post(self):
        return {"success": True, "route": 'toDo/post(create)'}

    def delete(self):
        return {"success": True, "route": 'toDo/delete'}
