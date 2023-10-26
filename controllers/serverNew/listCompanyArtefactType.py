from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify


class ListCompanyArtefactType(ClientAccess):
    def get(self,company_id):

        keys = ['id', 'company_id', 'artefact_type', 'description']
        sql = " SELECT * FROM company_artefact_types WHERE company_id = %s; "
        list_value = (company_id,)
        try:
            mycursor = mydb.cursor()
            mycursor.execute(sql, list_value)
            data_list = mycursor.fetchall()
            print("My Data", data_list)
            dictionary_data = [{key: value for key,
                                value in zip(keys, item)} for item in data_list]
            print("RESULT>>>", dictionary_data)
            return jsonify({'status': True, "msg": "Success", "data": dictionary_data})
        except Exception as e:
            print("My error in listCompanyArtefactType", e)
            return jsonify({"error": e, "status": False})