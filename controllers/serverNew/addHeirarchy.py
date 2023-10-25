from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify

class AddHeirarchy(ClientAccess):
    def get(self, project_id, heirName):
        sql = "INSERT INTO hierarchy_list (project_id,hierarchy_name) VALUES (%s,%s)"

        # value=(str(heirName))
        # print("value is: " + value)
        values = (project_id, heirName)
        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql, values)
        mydb.commit()
        # mycursor.close()
        sql = "SELECT LAST_INSERT_ID()"

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        heirarchyId = {"message": str(
            mycursor.fetchall()[0]).split('(')[1].split(',')[0]}
        # mycursor.close()
        return jsonify(heirarchyId)