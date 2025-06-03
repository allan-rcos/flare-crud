from typing import Optional

from flask_restx import Resource, marshal_with, fields, inputs, abort, Namespace
from flask_restx.reqparse import RequestParser, Argument
from werkzeug.security import generate_password_hash

from db.config import db
from db.models.users import Users
from decorators import auth


email_regex = inputs.regex(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

parser = RequestParser(trim=True, bundle_errors=True)
parser.add_argument(Argument(name='limit', type=int, location='args', help='Pagination limit is a Integer', default=10))
parser.add_argument(Argument(name='page', type=int, location='args', help='Pagination page is a Integer', default=1))

create_parser = parser.copy()
create_parser.add_argument(Argument(name='username', type=str, location='json', required=True, help='Username is mandatory'))
create_parser.add_argument(Argument(name='password', type=str, location='json', required=True, help='Password is mandatory'))
create_parser.add_argument(Argument(name='email', type=email_regex, location='json', required=True, help='Email is mandatory'))

update_parser = parser.copy()
update_parser.add_argument( Argument(name='username', type=str, location='json'))
update_parser.add_argument(Argument(name='password', type=str, location='json'))
update_parser.add_argument(Argument(name='email', type=email_regex, location='json', nullable=True))

delete_parser = parser.copy()
delete_parser.add_argument(Argument(name='username', type=str, location='args', required=True, help='Username is mandatory'))

namespace = Namespace('users', description='Users related operations')

iuser = namespace.model('User', {
    'id': fields.Integer(required=True, description='The user identifier'),
    'username': fields.String(required=True, description='The user username'),
    'email': fields.String(description='The user email'),
})


@namespace.route('/')
class UserResource(Resource):
    method_decorators = [auth, namespace.marshal_list_with(iuser)]

    @staticmethod
    def _all_limited(limit: Optional[int], page: Optional[int]):
        return Users.query.paginate(page=page, per_page=limit).items

    def get(self):
        args = parser.parse_args()
        return self._all_limited(limit=args['limit'], page=args['page'])

    def post(self):
        data = create_parser.parse_args()
        if data['username'] == 'admin':
            abort(400, message='Admin user already exists.')
        user = Users(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password'])
        )
        db.session.add(user)
        db.session.commit()
        return self._all_limited(limit=data['limit'], page=data['page']), 201

    def patch(self, user: Users):
        if user.username == 'admin':
            abort(400, message='Admin user can\'t be updates.')

        data = update_parser.parse_args()
        if(not data['username'] and not data['password'] and not data['email']):
            return self._all_limited(limit=data['limit'], page=data['page']), 204

        if (data['email']):
            user.email = data['email']

        if (data['username']):
            user.username = data['username']

        if (data['password']):
            user.password = generate_password_hash(data['password'])

        db.session.commit()

        return self._all_limited(limit=data['limit'], page=data['page'])

    def delete(self, user):
        args = delete_parser.parse_args()
        if user.username != args['username']:
            abort(400, message='Incorrect session username')

        db.session.delete(user)
        db.session.commit()

        return self._all_limited(limit=args['limit'], page=args['page'])
