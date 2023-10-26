from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify

# @ app.route('/getArtefactDefaults/<project_id>', methods=['GET', 'POST'])
class GetArtefactDefaults(ClientAccess):
    def get(self,project_id):
        sql = "SELECT * FROM  artefact_type_default;"
        print(sql)
        mydb.close()
        mydb.connect()
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