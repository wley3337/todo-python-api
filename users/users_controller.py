import os
import json
from flask import request
from flask_restful import Resource
import jwcrypto
from jwcrypto import jwt, jwk
from users import users_model


class UsersController(Resource):
    def get(self):
        user = users_model.all_users()
        return {"success": True, "users": user}, 200


# >>> from jwcrypto import jwt, jwk
# >>> k = {"k": "Wal4ZHCBsml0Al_Y8faoNTKsXCkw8eefKXYFuwTBOpA", "kty": "oct"}
# >>> key = jwk.JWK(**k)
# >>> e = token (unicode)
# >>> ET = jwt.JWT(key=key, jwt=e)
# >>> ST = jwt.JWT(key=key, jwt=ET.claims)
# >>> ST.claims
# u'{"info":"I\'m a signed token"}'

class UsersAutoLogin(Resource):
    def get(self):
        # print("key", key)
        token = request.headers["Authorization"].split(" ")[1][:-1]
        # token = make_encrypted_token()
        print("token: ", token)
        k = {"k": os.environ["SECRET_KEY"], "kty": "oct"}
        key = jwk.JWK(**k)
        print("key: ", key)

        njwt = jwt.JWT()
        # ET = jwt.JWT(key=key, jwt=token)
        # print("ET claims", ET.claims)
        # results = jwt.JWT(key=key, jwt=ET.claims)
        njwt.deserialize(key=key, jwt=token)
        u = njwt.claims
        # u = results.claims
        print("Decrypted Token: ", u)

        user = users_model.get_user_by_id(1)
        if user is None:
            return {"success": False, "errors": {"messages": ["User not found"]}}, 204
        return {"success": True, "user": user}, 200


def make_encrypted_token():
    pL = {"user_id": 1}
    k = {"k": os.environ["SECRET_KEY"], "kty": "oct"}
    key = jwk.JWK(**k)
    token = jwt.JWT(header={"alg": "HS256"},
                    claims=pL)
    token.make_signed_token(key)
    return token.serialize()
