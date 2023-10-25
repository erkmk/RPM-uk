from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify
import shutil
import json
from controllers.serverNew.openArtefact import OpenArtefact
import os
from pathlib import Path


class Artefact(ClientAccess):
    def post(self, contId):
        path_exist = "default"
        artefact = request.form['artInfo']
        artefact = json.loads(artefact)
        if (request.files):
            file = request.files['file']
        else:
            file = []
        if file:
            try:
                filename = file.filename
                Path(artefact['location_url'].split('artefacts')[
                    0] + 'templates').mkdir(parents=True, exist_ok=True)
                Path(artefact['location_url']).mkdir(parents=True, exist_ok=True)

                file.save(os.path.join(artefact['location_url'].split(
                    'artefacts')[0] + 'templates/', filename))
                shutil.copyfile(artefact['location_url'].split('artefacts')[0] + 'templates/' + filename,
                                artefact['location_url'] + artefact['artefact_name'].split('.')[0] + '.' + filename.split('.')[-1])
            except:
                message = {"message": 'urls not correct'}
                return jsonify(message)
        else:
            if (location_type == 'User defined default locations'):
                path_exist = OpenArtefact.get(artefact['location_url'], location_type)
                path_exist = path_exist.json['message']
                if path_exist == True:
                    # return jsonify({"message": 'url exists'})
                    path_exist = "default"
                if path_exist == False:
                    return jsonify({"message": 'URL do not exists'})

        if path_exist == "default":
            print(artefact)
            artId = artefact['artefact_id']
            del artefact['artefact_id']
            pairs = artefact.items()
            key = []
            value = []
            for k, v in pairs:
                key.append(str(k))
                value.append(str(v))
            key = tuple(key)
            value = tuple(value)
            print(value)
            if (artId == ""):
                sql = "INSERT INTO artefact (" + ", ".join(key) + \
                    ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                mydb.close()
                mydb.connect()
                mycursor = mydb.cursor()
                mycursor.execute(sql, value)
                mydb.commit()
                # mycursor.close()
                sql = "SELECT LAST_INSERT_ID()"

                mydb.close()
                mydb.connect()
                mycursor = mydb.cursor()
                mycursor.execute(sql)
                artefactId = {"message": str(
                    mycursor.fetchall()[0]).split('(')[1].split(',')[0]}
                # mycursor.close()
                # print(artefactId)
                if (contId != "root"):
                    value = (contId, artefactId['message'])
                    sql = "INSERT INTO container_artefact_link (container_id, artefact_id) VALUES (%s, %s)"

                    mydb.close()
                    mydb.connect()
                    mycursor = mydb.cursor()
                    mycursor.execute(sql, value)
                    mydb.commit()
                    # mycursor.close()
                # os.mkdir("/home/musab/RapidPMV2/artefacts/" + str(project['company_id']) + '/' + artefact['project_id'] + '/' + str(artefactId["message"]))
                message = {"message": 'success'}
                return jsonify(message)
            else:
                sql = "UPDATE artefact SET artefact_type = '" + str(artefact[
                    'artefact_type']) + "', artefact_owner = '" + str(
                    artefact['artefact_owner']) + "', artefact_name = '" + str(artefact['artefact_name']) + "', description = '" + \
                    str(artefact['description']) + "', status = '" + str(artefact['status']) + "',create_date = '" + str(
                    artefact[
                        'create_date']) + "',update_date = '" + str(artefact['update_date']) + "',location_url = '" + str(
                    artefact['location_url']) + "',template_url = '" + str(artefact['template_url']) + "',project_id = '" + str(
                    artefact['project_id']) + "',template = '" + str(artefact['template']) + "' WHERE artefact_id = '" + str(
                    artId) + "';"

                mydb.close()
                mydb.connect()
                mycursor = mydb.cursor()
                mycursor.execute(sql)
                mydb.commit()
                # mycursor.close()
                message = {"message": 'success'}
                return jsonify(message)

        else:
            return jsonify({"message": 'something went wrong make sure client is running'})