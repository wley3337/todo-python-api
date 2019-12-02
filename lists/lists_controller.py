from flask_restful import Resource


class ListsController(Resource):
    def post(self):
        return {"success": True, "route": "Lists/post(create)"}

    def delete(self):
        return {"success": True, "route": "Lists/delete"}
