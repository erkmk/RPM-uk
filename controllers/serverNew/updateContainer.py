from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify


class UpdateContainer(ClientAccess):
    def get(self,contTitle, contId):
        sql = "UPDATE hierarchy_container SET container_title = '" + str(contTitle) + "' WHERE container_id = '" + str(
            contId) + "';"

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
        # mycursor.close()
        return ({"message": "success"})