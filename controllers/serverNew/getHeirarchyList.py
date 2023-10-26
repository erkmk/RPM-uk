from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify


class GetHeirarchyList(ClientAccess):
    def get(self,project_id):
        sql = "SELECT * FROM hierarchy_list WHERE project_id = %s;"
        values = (project_id,)
        try:
            mycursor = mydb.cursor()
            mycursor.execute(sql, values)
            result = mycursor.fetchall()
        except Exception as e:
            return jsonify({'error': e, "status": False})
        # row_headers = [x[0] for x in mycursor.description]
        row_headers = ['hierarchy_id', 'hierarchy_name', 'project_id']

        result = [dict(zip(row_headers, res)) for res in result]
        print(result)
        return jsonify({"Data": result, "Status": True})
