from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify

# @ app.route('/getMembers/<company_id>', methods=['GET', 'POST'])
class GetMembers(ClientAccess):
    def get(self, company_id):
        sql = "SELECT u.user_id,u.name,u.email,u.status,r.company_role FROM user_company_role r INNER JOIN user u ON u.user_id = r.user_id WHERE r.company_id = '" + company_id + "';"

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