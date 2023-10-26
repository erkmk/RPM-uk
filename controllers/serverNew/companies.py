from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify


class Companies(ClientAccess):
    def get(self,):
        sql = "SELECT * FROM  company;"

        # mydb.close()
        # mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        result = mycursor.fetchall()
        header = mycursor.description
        # print(header)
        row_headers = [x[0] for x in mycursor.description]
        # mycursor.close()
        # print(row_headers)
        result = [dict(zip(row_headers, res)) for res in result]
        # users = {"message": result};
        print(result)
        return jsonify(result)