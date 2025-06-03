import os
from functools import wraps

import jwt
from flask import request
from flask_restx import abort

from db.models.users import find_by_username


def auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not auth.token:
            abort(403, message='Token is missing.')

        try:
            data = jwt.decode(auth.token, os.getenv('SECRET_KEY'), algorithms=os.getenv('TOKEN_ALGORITHM') or "HS256")
            current_user = find_by_username(data['username'])
        except Exception as exception:
            abort(400, message='Token is invalid or expired', exception=str(exception))
            return
        try:
            return f(*args, user=current_user, **kwargs)
        except TypeError:
            return f(*args, **kwargs)

    return decorated
