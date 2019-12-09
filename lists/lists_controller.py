from flask import request
from flask_restful import Resource
from util.jwt_handler import auth_decorator
from lists.lists_model import List, serialize_list_by_id, delete_list_by_id

import pdb


class ListsController(Resource):
    method_decorators = [auth_decorator]

    def post(self, user_id):
        """
        Creates a list under logged in user. Request body shape: {'list': {'heading': 'heading title'} }
        """
        r_body = request.get_json()
        heading = r_body["list"]["heading"]
        new_list = List(user_id, heading)
        if new_list.save():
            return {"success": True, "list": new_list.to_json()}, new_list.status_code
        else:
            print("newList Error: ", new_list)
            return {"success": False, "errors": new_list.errors}, new_list.status_code

    def delete(self, user_id, list_id):
        """
        Deletes a list under a logged in user. Request body shape: 

        Return deleted list
        """
        r_body = request.get_json()
        # this is to be sure no one can send just via the URL
        list_id_to_delete = r_body["list"]["id"]
        list_to_return = serialize_list_by_id(list_id_to_delete)
        delete_list_by_id(list_id_to_delete)
        return {"success": True, "list": list_to_return}, 200
