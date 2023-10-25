from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify

class TypeBulkAdd(ClientAccess):
    def post(self):
        typeDefaults = request.json
        for typeDefault in typeDefaults:
            print(typeDefault)
            typeId = typeDefault['type_id']
            del typeDefault['type_id']
            pairs = typeDefault.items()
            key = []
            value = []
            for k, v in pairs:
                key.append(str(k))
                value.append(str(v))
            key = tuple(key)
            value = tuple(value)
            print(value)
            if (typeId == ""):
                sql = "INSERT INTO artefact_type_default (" + ", ".join(
                    key) + ") VALUES (%s, %s, %s, %s, %s, %s)"
                try:
                    mydb.close()
                    mydb.connect()
                    mycursor = mydb.cursor()
                    mycursor.execute(sql, value)
                    mydb.commit()
                    mydb.cursor()
                except Exception as e:
                    print(e)
                # sql = "SELECT LAST_INSERT_ID()"
                # mycursor.execute(sql)
                # mydb.commit()
                # typeId = {"message": str(mycursor.fetchall()[0]).split('(')[1].split(',')[0]}
                # return jsonify(typeId)
            else:
                sql = "UPDATE artefact_type_default SET project_id = '" + str(
                    typeDefault['project_id']) + "', artefact_type = '" + typeDefault['artefact_type'] + "', location_url = '" + \
                    typeDefault['location_url'] + "', template_url = '" + typeDefault['template_url'] + "', multiples = '" + \
                    typeDefault['multiples'] + "', mandatory = '" + typeDefault['mandatory'] + "'WHERE type_id = '" + str(
                    typeId) + "';"
                # sql = "UPDATE user SET (" + ", ".join(key) + ") VALUES (%s, %s, %s, %s, %s, %s, %s) WHERE user_id = '" + str(custmId) + "';"
                try:
                    mydb.close()
                    mydb.connect()
                    mycursor = mydb.cursor()
                    mycursor.execute(sql)
                    mydb.commit()
                except Exception as e:
                    print(e)
                # mycursor.close()
        typeId = {"message": "successfull"}
        return jsonify(typeId)