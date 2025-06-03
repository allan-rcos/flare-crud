import os

from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from dotenv import load_dotenv

from db.config import config as db_config
# from resources import
from resources import AuthResource, UserNamespace

app = Flask(__name__)
cors = CORS(app)
api = Api(app, prefix=os.getenv('APPLICATION_ROOT') or '', catch_all_404s=True)
# To avoid SQL config exception
load_dotenv()
if not os.getenv('SECRET_KEY'):
    raise Exception('Secret key is mandatory')
db = db_config(app)

# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'

# api.add_resource(Hello, '/hello/')
api.add_namespace(UserNamespace)
api.add_resource(AuthResource, '/auth')

if __name__ == '__main__':
    app.run()
