from flask_jsonpify import jsonify

from controllers.auth import ClientAccess


class GetContainer(ClientAccess):
    def get(self,contId):
        # @ app.route('/getContainer/<contId>', methods=['GET', 'POST'])
        sql = "SELECT * FROM  hierarchy_container WHERE container_id = '" + contId + "';"

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