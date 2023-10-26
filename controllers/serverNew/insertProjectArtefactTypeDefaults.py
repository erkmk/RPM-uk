from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify

class InsertProjectArtefactTypeDefaults(ClientAccess):
    def post(self,project_id):

        insert_query = "INSERT INTO project_artefact_type_defaults (project_id, artefact_type,description,default_url,template_url,multiples,mandatory) VALUES (%s, %s,%s,%s,%s,%s,%s);"
        insert_value = (project_id, "", "", "", "","1","1")
        try:
            mycursor = mydb.cursor()
            mycursor.execute(insert_query, insert_value)
            mydb.commit()
            return jsonify({"status": True, "msg": "Project Artefact Type Data Added"})
        except Exception as e:
            print("My error in Project Artefact Type", e)
            return jsonify({"error": e, "status": False})
