from flask_restful import Resource 

class UsersController(Resource):
    def get(self):
        return {"connected": True}, 200



# def test1():
#     print("This works!")


