from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify


class DeleteType(ClientAccess):
    def get(self,type_id):
        # @ app.route('/deleteType/<type_id>', methods=['GET', 'POST'])
        sql = "DELETE FROM artefact_type_default WHERE type_id = '" + type_id + "';"

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
        # mycursor.close()
        return ({"message": "success"})