from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify

class CompaniesListDetails(ClientAccess):
    def get(self,userId):
        # @ app.route('/getCompaniessList/<userId>', methods=['GET', 'POST'])
        sql = " SELECT u.*, c.*, usr.rpm_admin FROM user_company_role u INNER JOIN company c ON u.company_id = c.company_id INNER JOIN user usr ON u.user_id = usr.user_id WHERE u.user_id = {} AND c.is_deleted = 0;".format(userId)
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