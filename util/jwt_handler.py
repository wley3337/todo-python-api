import os
import ast
from flask import request
from functools import wraps
from jwcrypto import jwt, jwk


def auth_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers["Authorization"].split(" ")[1][:-1]
        d_token = decrypt_token(token)
        user_id = d_token["user_id"]
        return func(*args, **kwargs, user_id=user_id)
    return wrapper


def decrypt_token(token):
    """
    Decrypts a JWT token (single encryption cycle) returns a dict
    """
    key = gen_key()
    new_jwt = jwt.JWT()
    new_jwt.deserialize(key=key, jwt=token)
    return ast.literal_eval(new_jwt.claims)


def make_encrypted_token(payload):
    """
    Creates a JWT Token (single encryption cycle) given a payload {'user_id': num}
    """
    key = gen_key()
    token = jwt.JWT(header={"alg": "HS256"},
                    claims=payload)
    token.make_signed_token(key)
    return token.serialize()


def gen_key():
    """
    Creates a JWT Key obj for encryption
    """
    k = {"k": os.environ["SECRET_KEY"], "kty": "oct"}
    return jwk.JWK(**k)
