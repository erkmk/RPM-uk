from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify

class AddContainer(ClientAccess):
    def get(containerName, root, projId, herId):
        print("heirarchyid: " + herId)
        if (root == "root"):
            value = (containerName, projId, herId)
            sql = "INSERT INTO hierarchy_container (container_title, project_id, hierarchy_id) VALUES (%s, %s, %s)"
        if (root != "root"):
            value = (containerName, projId, herId, root)
            sql = "INSERT INTO hierarchy_container (container_title, project_id, hierarchy_id, parent_container_id) VALUES (%s, %s, %s, %s)"

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql, value)
        mydb.commit()
        # mycursor.close()
        message = {"message": "success"}
        return jsonify(message)
