import os
from datetime import datetime, timedelta, timezone

import jwt
from flask import request
from flask_restx import Resource, marshal_with, fields, abort
from werkzeug.security import check_password_hash

from db.models.users import find_by_username


class AuthResource(Resource):

    @staticmethod
    def _encode_token(username: str):
        td = timedelta(seconds=int(os.getenv('TOKEN_EXPIRATION') or 3600))
        exp = datetime.now(tz=timezone.utc) + td
        return jwt.encode({
            'username': username,
            'exp': exp,
        }, os.getenv('SECRET_KEY'), algorithm=os.getenv('TOKEN_ALGORITHM') or "HS256"), datetime.now() + td

    @marshal_with({ 'token': fields.String, 'exp': fields.DateTime })
    def get(self):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            abort(400, message='Bad authorization')

        if auth.username == 'admin' and auth.password == 'admin':
            token, exp = self._encode_token('admin')
            print(exp)
            return { 'token': token, 'exp': exp }

        user = find_by_username(auth.username)

        if not user:
            abort(404, message='User not found')

        if not check_password_hash(user.password, auth.password):
            abort(401)

        token, exp = self._encode_token(user.username)
        return { 'token': token, 'exp': exp }
