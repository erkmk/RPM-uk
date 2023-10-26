from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify


class GetHeirarchyListData(ClientAccess):
    def get(self):
        sql = "SELECT * FROM hierarchy_list "
        try:
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            result = mycursor.fetchall()
        except Exception as e:
            return jsonify({'error': e, "status": False})
        # row_headers = [x[0] for x in mycursor.description]
        row_headers = ['hierarchy_id', 'hierarchy_name', 'project_id']

        result = [dict(zip(row_headers, res)) for res in result]
        print(result)
        return jsonify({"Data": result, "Status": True})
