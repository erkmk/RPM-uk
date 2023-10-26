
from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify

# @ app.route('/getprojects/<company_id>', methods=['GET', 'POST'])
class Projects(ClientAccess):
    def get(self,company_id):
        sql = "SELECT * FROM  project WHERE company_id = '" + company_id + "';"

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        result = mycursor.fetchall()
        print(result)
        header = mycursor.description
        # print(header)
        row_headers = [x[0] for x in mycursor.description]
        # mycursor.close()
        # print(row_headers)
        result = [dict(zip(row_headers, res)) for res in result]
        # users = {"message": result};
        print("Project --->>>>Company Type",result)
        return jsonify(result)
