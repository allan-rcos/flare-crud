import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources import HelloWorld

app = Flask(__name__)
cors = CORS(app)
api = Api(app, prefix=os.getenv('APPLICATION_ROOT') or '', catch_all_404s=True)

# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'

api.add_resource(HelloWorld, '/hello/')

if __name__ == '__main__':
    app.run()
