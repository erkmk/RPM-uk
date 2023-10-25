from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify


class Type(ClientAccess):
    def post(self):
        typeDefault = request.json
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
                # mycursor.close()
            except Exception as e:
                print(e)
            sql = "SELECT LAST_INSERT_ID()"
            try:
                mydb.close()
                mydb.connect()
                mycursor = mydb.cursor()
                mycursor.execute(sql)
                typeId = {"message": str(mycursor.fetchall()[0]).split(
                    '(')[1].split(',')[0]}
                # mycursor.close()
            except Exception as e:
                print(e)
            return jsonify(typeId)
        else:
            sql = "UPDATE artefact_type_default SET project_id = '" + str(typeDefault['project_id']) + "', artefact_type = '" + \
                typeDefault['artefact_type'] + "', location_url = '" + typeDefault['location_url'] + "', template_url = '" + \
                typeDefault['template_url'] + "', multiples = '" + typeDefault['multiples'] + "', mandatory = '" + \
                typeDefault['mandatory'] + \
                "'WHERE type_id = '" + str(typeId) + "';"
            # sql = "UPDATE user SET (" + ", ".join(key) + ") VALUES (%s, %s, %s, %s, %s, %s, %s) WHERE user_id = '" + str(custmId) + "';"
            try:
                mydb.close()
                mydb.connect()
                mycursor = mydb.cursor()
                mycursor.execute(sql)
                mydb.commit()
                mydb.cursor()
                typeId = {"message": str(typeId)}
            except Exception as e:
                print(e)
            return jsonify(typeId)