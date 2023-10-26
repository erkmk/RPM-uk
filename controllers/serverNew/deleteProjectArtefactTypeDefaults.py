from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify


class DeleteProjectArtefactTypeDefaults(ClientAccess):
    def post(self,id_):
        delete_query = " DELETE FROM project_artefact_type_defaults WHERE id = %s ;"
        delete_value = (id_,)

        try:
            mycursor = mydb.cursor()
            mycursor.execute(delete_query, delete_value)
            mydb.commit()
            return jsonify({"status": True, "msg": "Project Artefact Type Default Data Deleted"})
        except Exception as e:
            print("Error updating updateProjectArtefactTypeDefaults", e)
            return jsonify({"error": e, "status": False})
