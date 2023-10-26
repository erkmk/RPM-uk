from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify


class InsertCompanyArtefactType(ClientAccess):
    def post(self,company_id):

        insert_query = "INSERT INTO company_artefact_types (company_id, artefact_type,description) VALUES (%s, %s,%s)"
        insert_value = (company_id, "", "")
        try:
            mycursor = mydb.cursor()
            mycursor.execute(insert_query, insert_value)
            mydb.commit()
            return jsonify({"status": True, "msg": "Company Artefact Type Data Added"})
        except Exception as e:
            print("My error in insertCompanyArtefactType", e)
            return jsonify({"error": e, "status": False})

        return jsonify({"status": False, "msg": "Duplicate Entry Not Allowed"})