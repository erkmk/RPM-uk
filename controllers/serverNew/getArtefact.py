from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify



class GetArtefact(ClientAccess):
    def get(self,artId):
        # @ app.route('/getArtefact/<artId>', methods=['GET', 'POST'])

        sql_fetch_location = "SELECT p.location_url FROM artefact a JOIN project p ON a.project_id = p.project_id WHERE a.artefact_id = {};".format(98)
        try:
            mycursor = mydb.cursor()
            mycursor.execute(sql_fetch_location)
            location_url = mycursor.fetchall()[0][0]
        except Exception as e:
            print('error is e1', e)
        
        
        sql = "SELECT * FROM  artefact WHERE artefact_id = '" + artId + "';"
        try:
            mydb.connect()
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            result = mycursor.fetchall()
            header = mycursor.description
        except Exception as e:
            print('error is e', e)
        # print(header)
        row_headers = [x[0] for x in mycursor.description]
        # mycursor.close()
        # print(row_headers)
        result = [dict(zip(row_headers, res)) for res in result]
        # users = {"message": result};
        print("Artefact Result",result)
        if location_url:
            result[0]['location_url'] = location_url
            print("After Modify--->>>>",result)
        return jsonify(result)