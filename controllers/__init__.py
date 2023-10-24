from flask import Blueprint
from flask_restful import Api
from controllers.serverNew.login import Login


server_blueprint = Blueprint("server", __name__)

api = Api(server_blueprint)
api.add_resource(Login, "/login/<userEmail>/<userPassword>'")