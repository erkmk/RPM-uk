from controllers.auth import ClientAccess
import json
import jwt
from common_util import checkLogin
import os
from flask_jsonpify import jsonify
import shutil


class OpenArtefact(ClientAccess):
    def get(self, artId, location_type):
        combinedData = {}
        global users
        try:
            if Login():
                import serverTest
                if users:
                    if not location_type == "User defined default locations":
                        sql = "SELECT * FROM artefact WHERE artefact_id = '" + artId + "';"
                        try:
                            mydb.close()
                            mydb.connect()
                            mycursor = mydb.cursor()
                            mycursor.execute(sql)
                            result = mycursor.fetchall()
                            # mycursor.close()
                            row_headers = [x[0] for x in mycursor.description]

                            combinedData = [dict(zip(row_headers, res))
                                        for res in result]
                            combinedData = combinedData[0]
                        except Exception as e:
                            print(e)
                else:
                    raise Exception()
                try:
                    if (combinedData['artefact_name'] + '.docx' not in os.listdir(combinedData['location_url'])):
                        shutil.copy(os.path.join(combinedData['template_url']),
                                    os.path.join(combinedData['location_url'], combinedData['artefact_name'] + '.docx'))
                except:
                    if (location_type == 'User defined default locations'):
                        combinedData['location_type'] = artId
                        return jsonify({"message": serverTest.server(str(combinedData), users["connection"])})
                    # else:
                    #   return jsonify({"message": "file not found"})
                combinedData['downloadType'] = 'artefact'
                combinedData = json.dumps(combinedData)
                combinedData = json.loads(combinedData)
                message = {"message": "open request sent to client"}
                print(str(combinedData))
                serverTest.server(str(combinedData), users["connection"])
                return jsonify(message)
            else:
                users = {}
                raise Exception()
        except:
            return jsonify({"message": "make sure client is running"})