from flask import Blueprint
from controllers.serverNew.addHeirarchy import AddHeirarchy
from controllers.serverNew.artefact import Artefact
from controllers.serverNew.company import Company
from controllers.serverNew.download import Download
from controllers.serverNew.openArtefact import OpenArtefact
from controllers.serverNew.project import Project
from controllers.serverNew.typeBulkAdd import TypeBulkAdd
from controllers.serverNew.upload import Upload
from controllers.serverNew.user import User
from controllers.serverNew.type import Type
from flask_restful import Api
from controllers.serverNew.login import Login


server_blueprint = Blueprint("server", __name__)

api = Api(server_blueprint)
api.add_resource(Login, "/login/<userEmail>/<userPassword>")
api.add_resource(OpenArtefact, "/openArtefact/<artId>/<location_type>")
api.add_resource(Download, "/download/<loc>/<name>")
api.add_resource(Upload, "/upload")
api.add_resource(Company, "/company")
api.add_resource(User, "/user")
api.add_resource(Type, "/type")
api.add_resource(TypeBulkAdd, "/typeBulkAdd")
api.add_resource(Project, "/project")
api.add_resource(Artefact, "/artefact/<contId>")
api.add_resource(AddHeirarchy, "/addHeirarchy/<project_id>/<heirName>")
