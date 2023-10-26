from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify

class ListProjectArtefactTypeDefaults(ClientAccess):
    def get(self,project_id):

        keys = ['project_id', 'artefact_type', 'description',
                'default_url', 'template_url', 'multiples', 'mandatory', 'id', 'c_id']
        sql = " SELECT p.project_id,c.artefact_type,c.description,p.default_url,p.template_url,p.multiples,p.mandatory,p.id,c.id as c_id FROM project_artefact_type_defaults p LEFT JOIN company_artefact_types c ON c.id = p.artefact_type WHERE p.project_id = %s; "
        list_value = (project_id,)
        print("SQL STATEMENT", sql)
        try:
            mycursor = mydb.cursor()
            mycursor.execute(sql, list_value)
            data_list = mycursor.fetchall()
            print("My Data", data_list)
            dictionary_data = [{key: value for key,
                                value in zip(keys, item)} for item in data_list]
            print("RESULT>>>", dictionary_data)
            return jsonify({'status': True, "msg": "success", "data": dictionary_data})
        except Exception as e:
            print("My error in listProjectArtefactType", e)
            return jsonify({"error": e, "status": False})