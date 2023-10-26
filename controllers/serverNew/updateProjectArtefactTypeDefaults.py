from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify

class UpdateProjectArtefactTypeDefaults(ClientAccess):
    def post(self):

        if request.method == 'POST':
            id_ = request.form.get('id')
            project_id = request.form.get('project_id')
            artefact_type = request.form.get('artefact_type')
            description = request.form.get('description')
            default_url = request.form.get('default_url')
            template_url = request.form.get('template_url')
            multiples = request.form.get('multiples')
            mandatory = request.form.get('mandatory')

        update_query = "UPDATE  project_artefact_type_defaults SET artefact_type = %s, description = %s, default_url = %s,template_url = %s, multiples = %s,mandatory = %s WHERE id = %s;"
        update_value = (artefact_type, description, default_url,
                        template_url, multiples, mandatory, id_)
        # print("update query>>>>>>>>>", update_query)
        try:
            mycursor = mydb.cursor()
            mycursor.execute(update_query, update_value)
            mydb.commit()
            return jsonify({"status": True, "msg": "Project Artefact Type Default Data Updated"})
        except Exception as e:
            print("Error updating updateProjectArtefactTypeDefaults", e)
            return jsonify({"error": e, "status": False})

