from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify

class CompaniesDetails(ClientAccess):
    def get(self,companyId):
        # @ app.route('/getCompaniess/<companyId>', methods=['GET', 'POST'])
        sql = " SELECT * FROM  company "
        if companyId != "":
            sql += " WHERE company_id = '"+companyId+"' "
        sql += ";"

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