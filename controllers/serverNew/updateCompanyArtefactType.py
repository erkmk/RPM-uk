from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify


class UpdateCompanyArtefactType(ClientAccess):
    def post(self):

        if request.method == 'POST':
            id_ = request.form.get('id')
            company_id = request.form.get('company_id')
            artefact_type = request.form.get('artefact_type')
            description = request.form.get('description')

        update_query = "UPDATE company_artefact_types SET artefact_type = %s, description = %s WHERE id = %s;"
        update_value = (artefact_type, description, id_)

        try:
            mycursor = mydb.cursor()
            mycursor.execute(update_query, update_value)
            mydb.commit()
            return jsonify({"status": True, "msg": "Company Artefact Type Data Updated"})
        except Exception as e:
            print("Error updating updateCompanyArtefactType", e)
            return jsonify({"error": e, "status": False})