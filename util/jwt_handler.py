from flask import request


def auth_decorator(func):
    def auth(*args, **kwargs):
        token = request.headers["Authorization"].split(" ")[1]
        print("token: ", token)
        func(*args, **kwargs)
    return auth
