from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify



class TokenDataDetails(ClientAccess):
    def get(self,tokenId):
        # @ app.route('/getTokenDataDetails/<tokenId>', methods=['GET', 'POST'])
        sql = "SELECT t.accessToken,u.email,u.name,u.user_id,u.firstLogin,u.verified FROM  tbl_microsoft_tokens t LEFT JOIN user u ON u.email=t.email WHERE t.id = '" + \
            tokenId + "' and t.current_status = 1;"

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