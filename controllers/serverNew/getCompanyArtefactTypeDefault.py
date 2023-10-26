from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify

class GetCompanyArtefactTypeDefault(ClientAccess):
    def get(self,project_id):
        keys = ['id', 'artefact_type']
        sql = "SELECT p.id,c.artefact_type FROM project_artefact_type_defaults p LEFT JOIN company_artefact_types c ON p.artefact_type = c.id WHERE p.project_id = %s"
        values = (project_id,)
        try:
            mycursor.execute(sql, values)
            data_list = mycursor.fetchall()
            print("My Data", data_list)
            dictionary_data = [{key: value for key,
                                value in zip(keys, item)} for item in data_list]
            print("RESULT>>>", dictionary_data)
            return jsonify({'status': True, 'data': dictionary_data})
        except Exception as e:
            print("My error in Project Artefact Type", e)
            return jsonify({"error": e, "status": False})