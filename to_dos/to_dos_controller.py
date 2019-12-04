from flask_restful import Resource
from to_dos import to_dos_model


class ToDosController(Resource):
    def post(self):
        return {"success": True, "route": 'toDo/post(create)'}

    def delete(self):
        return {"success": True, "route": 'toDo/delete'}
