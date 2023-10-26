from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify


class DeleteCompanyArtefactType(ClientAccess):
    def post(self,row_id):

        delete_query = " DELETE FROM company_artefact_types WHERE id = %s "
        delete_value = (row_id,)

        try:
            mycursor = mydb.cursor()
            mycursor.execute(delete_query, delete_value)
            mydb.commit()
            return jsonify({"status": True, "msg": "Company Artefact Type Data Deleted"})
        except Exception as e:
            print("Error updating updateCompanyArtefactType", e)
            return jsonify({"error": e, "status": False})