from flask import Blueprint
from controllers.serverNew.addHeirarchy import AddHeirarchy
from controllers.serverNew.admin import Admin
from controllers.serverNew.artefact import Artefact
from controllers.serverNew.companies import Companies
from controllers.serverNew.companies_details import CompaniesDetails
from controllers.serverNew.companies_list_details import CompaniesListDetails
from controllers.serverNew.company import Company
from controllers.serverNew.deletetype import DeleteType
from controllers.serverNew.download import Download
from controllers.serverNew.getArtefact import GetArtefact
from controllers.serverNew.getArtefactDefaults import GetArtefactDefaults
from controllers.serverNew.getArtefacts import GetArtefacts
from controllers.serverNew.getMembers import GetMembers
from controllers.serverNew.getProject import GetProjetc
from controllers.serverNew.getUsers import GetUsers
from controllers.serverNew.openArtefact import OpenArtefact
from controllers.serverNew.project import Project
from controllers.serverNew.projects import Projects
from controllers.serverNew.token_data import TokenData
from controllers.serverNew.token_data_details import TokenDataDetails
from controllers.serverNew.token_data_verify import TokenDataVrify
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
api.add_resource(GetUsers, "/getUsers/<company_id>")
api.add_resource(GetMembers, "/getMembers/<company_id>")
api.add_resource(GetArtefactDefaults, "/getArtefactDefaults/<project_id>")
api.add_resource(Projects, "/getprojects/<company_id>")
api.add_resource(Companies, "/getCompanies")
api.add_resource(CompaniesDetails, "/getCompaniess/<companyId>")
api.add_resource(CompaniesListDetails, "/getCompaniessList/<userId>")
api.add_resource(DeleteType, "/deleteType/<type_id>")
api.add_resource(GetProjetc, "/getProject/<projectId>")
api.add_resource(Admin, "/getAdmin/<companyId>")
api.add_resource(TokenData, "/getTokenData/<tokenId>")
api.add_resource(TokenDataVrify, "/verifyTokenData")
api.add_resource(TokenDataDetails, "/getTokenDataDetails/<tokenId>")
api.add_resource(GetArtefacts, "/getArtefacts/<projectId>")
api.add_resource(GetArtefact, "/getArtefact/<artId>")



