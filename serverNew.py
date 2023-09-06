from datetime import date
import os

import mysql.connector
import secrets
from flask import Flask, request, send_file, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask_cors import CORS
from flask_jsonpify import jsonify
import json
import jwt
import smtplib
# import ssl
import math
import random
import socket
import glob
import os.path
import shutil
from pathlib import Path
from generate_jwt import jwtToken
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
# api = Api(app)
CORS(app, origins="*")

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_USERNAME'] = 'samreshkumarjha21@outlook.com'
app.config['MAIL_USERNAME'] = 'rapidPMV2@outlook.com'
app.config['MAIL_PASSWORD'] = 'Alchemist21@#'
# app.config['MAIL_TIMEOUT'] = 60
app.config['SECRET_KEY'] = 'secret'

mail = Mail(app)

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])


# app.secret_key = b'wellThisIsMySecreteKey'
# socket.setdefaulttimeout(1)
# soc = socket.socket()
# host = '0.0.0.0'  # The server's hostname or IP address
# port = 2004  # The port used by the server


# @app.before_first_request
# def do_something_only_once():
#     # comSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     soc.bind((host, port))
#     soc.listen(5)


users = {}

# MySQL #######3
# initializing database connection
mydb = mysql.connector.connect(
    host="82.69.10.205",
    user="musab",
    password="RAPIDPM",
    database="RPMnew_dataBase",
    auth_plugin='mysql_native_password'
)

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="teckvalley2",
#     password="pass@123!!fefwW231",
#     database="artefacts",

# )
ret = ""
# defining cursor to navigate through databas

mycursor = mydb.cursor()
mycursor = mydb.cursor(buffered=True)

######### Login ###########


# def Login():
#     global users
#     try:
#         print("checking connection1")
#         conn, addr = soc.accept()
#         print("checking connection2")
#         if (conn):
#             print("Got connection from", addr)
#             length_of_message = int.from_bytes(conn.recv(2), byteorder='big')
#             msg = conn.recv(length_of_message).decode("UTF-8")
#             print(msg)
#             users["connection"] = conn
#         return True
#     except socket.timeout:
#         connec = users["connection"]
#         if connec:
#             initialMsg = "you still there?".encode("UTF-8")
#             connec.send(len(initialMsg).to_bytes(2, byteorder='big'))
#             connec.send(initialMsg)

#             length_of_message = int.from_bytes(connec.recv(2), byteorder='big')
#             initialResponse = connec.recv(length_of_message).decode("UTF-8")
#             if (initialResponse == "yes"):
#                 print("client is still running")
#             else:
#                 return False
#         print("time out")
#         return True


#### functions #####
def checkLogin(userEmail, userPassword):
    query = "SELECT cu.password, co.RPM, co.company_id, cu.user_id, cu.company_role FROM user cu, company co WHERE cu.email = '" + \
        userEmail + "' and cu.company_id = co.company_id;"
    try:
        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(query)
        result = mycursor.fetchall()
    except Exception as e:
        print(e)
    # mycursor.close()
    json_data = {}
    if (result):
        print(result)
        if (result[0][0] == userPassword):
            if (result[0][1] != "Yes"):
                json_data["authorized"] = "True"
                json_data["RPM"] = "False"
                json_data["message"] = ["Welcome"]
                json_data["compId"] = [result[0][2]]
                json_data["id"] = [result[0][3]]
                json_data["role"] = [result[0][4]]
            else:
                json_data["authorized"] = "True"
                json_data["RPM"] = "True"
                json_data["message"] = ["Welcome RPM"]
                json_data["compId"] = [result[0][2]]
                json_data["id"] = [result[0][3]]
                json_data["role"] = [result[0][4]]
        else:
            json_data["authorized"] = "False"
            json_data["RPM"] = "RPM"
            json_data["message"] = ["Incorrect password"]
            json_data["compId"] = ["compId"]
            json_data["id"] = ["id"]
            json_data["role"] = ["role"]
    else:
        json_data["authorized"] = "False"
        json_data["message"] = ["Email address not found"]
    return (json.dumps(json_data), json_data)


@app.route('/openArtefact/<artId>/<location_type>', methods=['GET', 'POST'])
def openArtefact(artId, location_type):
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


@app.route('/download/<loc>/<name>', methods=['GET', 'POST'])
def download(loc, name):
    print("inside download endpoint")
    path = loc.replace("\\", "/") + name
    # if(name == "template"):
    #   path = loc.split("-")[1].replace("\\","/")
    # path = "C:\\RapidPM\\RapidPM\\a10-exception-report-v101.docx"
    # try:
    return send_file(path, as_attachment=True)
    # except:
    #   return 'not a server file'


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    print("inside upload endpoint")
    f = request.files['videoFile']
    print(f)
    # tempUrl = request.form["title"]
    # tempUrl = "/home/jc/RapidPM/RapidPM/" + tempUrl
    # fileType = request.form["description"]
    # id = request.form["id"]
    locationUrl = request.form["location"]
    if f:
        # if(fileType == "template"):
        #   pid = request.form["projectId"]
        #   sql = "INSERT INTO projects_artefactTypeDefault (ArtefactType, TemplateUrl, LocationUrl, Manadatory, Multiples, project_id)(SELECT ArtefactType, '" + "s-" + tempUrl.replace("\\\\","/") + "', LocationUrl, Manadatory, Multiples, '" + pid + "' FROM projects_artefactTypeDefault WHERE artefactType_id ='" + id + "')"
        #   mycursor.execute(sql)
        #   mydb.commit()
        #   sql = "INSERT INTO ProjectsTemplates (project_id, artefactType_id) VALUES (%s, %s)"
        #   cust = (int(pid), mycursor.lastrowid)
        #   mycursor.execute(sql, cust)
        #   mydb.commit()
        #   f.save(tempUrl.replace("\\\\","/"))
        # else:
        f.save(locationUrl + f.filename)
        return "Success"


@app.route('/login/<userEmail>/<userPassword>', methods=['GET', 'POST'])
def login(userEmail, userPassword):
    ret, json_data = checkLogin(userEmail, userPassword)
    print(ret)
    if (json_data["authorized"] == "True"):
        encoded_jwt = jwt.encode(
            {"email": userEmail, "password": userPassword,
                "usrId": json_data["id"], "compId": json_data["compId"]}, "secret",
            algorithm="HS256")
        print(encoded_jwt)
        json_data["jwt"] = str(encoded_jwt)
        ret = json.dumps(json_data)
    return (ret)


@app.route('/company', methods=['GET', 'POST'])
def company():
    company = request.json
    print(company)
    compId = company['company_id']
    del company['company_id']
    pairs = company.items()
    key = []
    value = []
    for k, v in pairs:
        key.append(str(k))
        value.append(str(v))
    key = tuple(key)
    value = tuple(value)
    print(value)
    if (compId == ""):
        try:
            sql = "INSERT INTO company (" + ", ".join(key) + \
                ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            mydb.close()
            mydb.connect()
            mycursor = mydb.cursor()
            mycursor.execute(sql, value)
            mydb.commit()
        except Exception as e:
            print(e)
        # mycursor.close()

        sql = "SELECT LAST_INSERT_ID()"
        try:
            mydb.close()
            mydb.connect()
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            companyId = {"message": str(
                mycursor.fetchall()[0]).split('(')[1].split(',')[0]}
        # mycursor.close()
        except Exception as e:
            print(e)
        os.mkdir("/home/musab/RapidPMV2/artefacts/" + companyId["message"])
        return jsonify(companyId)
    else:
        sql = "UPDATE company SET RPM = '" + value[0] + "', company_name = '" + value[1] + "', contact_name = '" + value[
            2] + "', address_line1 = '" + value[
            3] + "', address_line2 = '" + value[4] + "', address_line3 = '" + value[5] + "', city = '" + value[
            6] + "',country = '" + \
            value[7] + "',postal_code = '" + value[8] + \
            "' WHERE company_id = '" + str(compId) + "';"
        # sql = "UPDATE user SET (" + ", ".join(key) + ") VALUES (%s, %s, %s, %s, %s, %s, %s) WHERE user_id = '" + str(custmId) + "';"
        try:
            mydb.close()
            mydb.connect()
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            mydb.commit()
        # mycursor.close()
        except Exception as e:
            print(e)
        companyId = {"message": str(compId)}
        return jsonify(companyId)
    #
    # sql = "INSERT INTO company (" + ", ".join(key) + ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    # mycursor.execute(sql, value)
    # mydb.commit()
    # sql = "SELECT LAST_INSERT_ID()"
    # mycursor.execute(sql)
    # companyId = {"message": str(mycursor.fetchall()[0]).split('(')[1].split(',')[0]};
    # return jsonify(companyId)
    # # return ({"message": "customer received"})


@app.route('/user', methods=['GET', 'POST'])
def user():
    customer = request.json
    print(customer)
    custmId = customer['user_id']
    del customer['user_id']
    pairs = customer.items()
    key = []
    value = []
    for k, v in pairs:
        key.append(str(k))
        value.append(str(v))
    key = tuple(key)
    value = tuple(value)
    print(value)
    if (custmId == ""):
        sql = "INSERT INTO user (" + ", ".join(key) + \
            ") VALUES (%s, %s, %s, %s, %s, %s, %s)"
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
            customerId = {"message": str(
                mycursor.fetchall()[0]).split('(')[1].split(',')[0]}
        # mycursor.close()
        except Exception as e:
            print(e)
        return jsonify(customerId)
    else:
        sql = "UPDATE user SET company_id = '" + customer['company_id'] + "', company_role = '" + customer[
            'company_role'] + "', email = '" + customer['email'] + "', name = '" + customer['name'] + "', password = '" + \
            customer['password'] + "', status = '" + customer['status'] + "',verified = '" + customer[
            'verified'] + "' WHERE user_id = '" + str(custmId) + "';"
        # sql = "UPDATE user SET (" + ", ".join(key) + ") VALUES (%s, %s, %s, %s, %s, %s, %s) WHERE user_id = '" + str(custmId) + "';"
        try:
            mydb.close()
            mydb.connect()
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            mydb.commit()
            # mycursor.close()
        except Exception as e:
            print(e)
        customerId = {"message": str(custmId)}
        return jsonify(customerId)


@app.route('/type', methods=['GET', 'POST'])
def type():
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


@app.route('/typeBulkAdd', methods=['GET', 'POST'])
def typeBulkAdd():
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


@app.route('/project', methods=['GET', 'POST'])
def project():
    project = request.json
    print(project)
    projId = project['project_id']
    del project['project_id']
    pairs = project.items()
    key = []
    value = []
    for k, v in pairs:
        key.append(str(k))
        value.append(str(v))
    key = tuple(key)
    value = tuple(value)
    print(value)
    if (projId == ""):
        sql = "INSERT INTO project (" + ", ".join(key) + \
            ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
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
            projectId = {"message": str(
                mycursor.fetchall()[0]).split('(')[1].split(',')[0]}
        except Exception as e:
            print(e)
        # mycursor.close()
        # os.mkdir("/home/ubuntu/olddisk/var/www/html/im_Flask/RPM_/artefacts/" +
        #          str(project['company_id']) + '/' + str(projectId["message"]))
        os.makedirs("/home/samresh/Downloads/RPM_02-06-2023/artefacts/" +
                    str(project['company_id']) + '/' + str(projectId["message"]), exist_ok=True)
        return jsonify(projectId)
    else:
        sql = "UPDATE project SET project_name = '" + str(project[
            'project_name']) + "', template = '" + str(
            project['template']) + "', status = '" + str(project['status']) + "', owner = '" + str(project['owner']) + "', start = '" + str(project['start']) + "',end = '" + str(project[
                'end']) + "',hierarchy_id_default = '" + str(
            project['hierarchy_id_default']) + "' WHERE project_id = '" + str(projId) + "';"
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
        customerId = {"message": str(projId)}
        return jsonify(customerId)


@ app.route('/artefact/<contId>', methods=['GET', 'POST'])
def artefact(contId):
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
            path_exist = openArtefact(artefact['location_url'], location_type)
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


@ app.route('/addHeirarchy/<project_id>/<heirName>', methods=['GET', 'POST'])
def addHeirarchy(project_id, heirName):
    sql = "INSERT INTO hierarchy_list (project_id,hierarchy_name) VALUES (%s,%s)"

    # value=(str(heirName))
    # print("value is: " + value)
    values = (project_id, heirName)
    mydb.close()
    mydb.connect()
    mycursor = mydb.cursor()
    mycursor.execute(sql, values)
    mydb.commit()
    # mycursor.close()
    sql = "SELECT LAST_INSERT_ID()"

    mydb.close()
    mydb.connect()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    heirarchyId = {"message": str(
        mycursor.fetchall()[0]).split('(')[1].split(',')[0]}
    # mycursor.close()
    return jsonify(heirarchyId)


@ app.route('/getUsers/<company_id>', methods=['GET', 'POST'])
def getUsers(company_id):
    sql = "SELECT * FROM user WHERE company_id = '" + company_id + "';"

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


@ app.route('/getMembers/<company_id>', methods=['GET', 'POST'])
def getMembers(company_id):
    sql = "SELECT u.user_id,u.name,u.email,u.status,r.company_role FROM user_company_role r INNER JOIN user u ON u.user_id = r.user_id WHERE r.company_id = '" + company_id + "';"

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


@ app.route('/getArtefactDefaults/<project_id>', methods=['GET', 'POST'])
def getArtefactDefaults(project_id):
    # sql = "SELECT * FROM  artefact_type_default WHERE project_id = '" + project_id + "';"
    sql = "SELECT * FROM  artefact_type_default;"
    print(sql)
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


@ app.route('/getUser/<user_id>', methods=['GET', 'POST'])
def getUser(user_id):
    sql = "SELECT * FROM  user WHERE user_id = '" + user_id + "';"

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


@ app.route('/getprojects/<company_id>', methods=['GET', 'POST'])
def getprojects(company_id):
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
    print(result)
    return jsonify(result)


@ app.route('/getCompanies', methods=['GET', 'POST'])
def getCompanies():
    sql = "SELECT * FROM  company;"

    # mydb.close()
    # mydb.connect()
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


@ app.route('/getCompaniess/<companyId>', methods=['GET', 'POST'])
def getCompaniesDetails(companyId):
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


@ app.route('/getCompaniessList/<userId>', methods=['GET', 'POST'])
def getCompaniesListDetails(userId):
    sql = " SELECT * FROM  user_company_role u INNER JOIN  company c on u.company_id = c.company_id where u.user_id ='" + \
        userId+"' AND c.is_deleted=0 ;"
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


@ app.route('/deleteType/<type_id>', methods=['GET', 'POST'])
def deleteType(type_id):
    sql = "DELETE FROM artefact_type_default WHERE type_id = '" + type_id + "';"

    mydb.close()
    mydb.connect()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    # mycursor.close()
    return ({"message": "success"})


# @ app.route('/deleteUser/<user_id>', methods=['GET', 'POST'])
# def deleteUser(user_id):
#     sql = "DELETE FROM user WHERE user_id = '" + user_id + "';"

#     mydb.close()
#     mydb.connect()
#     mycursor = mydb.cursor()
#     mycursor.execute(sql)
#     mydb.commit()
#     # mycursor.close()
#     return ({"message": "success"})


# @ app.route('/deleteProject/<project_id>', methods=['GET', 'POST'])
# def deleteProject(project_id):
#     sql = "DELETE FROM project WHERE project_id = '" + project_id + "';"
#     try:

#         mydb.close()
#         mydb.connect()
#         mycursor = mydb.cursor()
#         mycursor.execute(sql)
#         mydb.commit()
#         # mycursor.close()
#         return ({"message": "success"})
#     except:
#         return ({"message": "failed"})


# @ app.route('/deleteCompany/<company_id>/<user_id>', methods=['GET', 'POST'])
# def deleteCompany(company_id, user_id):
#     print("trying to delete company: " + company_id)
#     sql = "DELETE FROM company WHERE company_id = '" + company_id + "';"
#     try:

#         mydb.close()
#         mydb.connect()
#         mycursor = mydb.cursor()
#         mycursor.execute(sql)
#         mydb.commit()
#         # mycursor.close()
#     except:
#         return ({"message": "failed"})
#     sql = "DELETE FROM user_company_role WHERE company_id = '" + \
#         company_id + "' AND user_id = '" + user_id + "';"
#     try:

#         mydb.close()
#         mydb.connect()
#         mycursor = mydb.cursor()
#         mycursor.execute(sql)
#         mydb.commit()
#         # mycursor.close()
#         return ({"message": "success"})
#     except:
#         return ({"message": "failed"})


@ app.route('/getCompany/<companyId>', methods=['GET', 'POST'])
def getCompany(companyId):
    sql = "SELECT c.*,u.user_id,u.email,u.name FROM  company c LEFT JOIN user u ON u.company_id = c.company_id WHERE c.company_id = '" + \
        companyId + "'"

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


@ app.route('/getProject/<projectId>', methods=['GET', 'POST'])
def getProject(projectId):
    sql = "SELECT * FROM  project WHERE project_id = '" + projectId + "';"

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


@ app.route('/getAdmin/<companyId>', methods=['GET', 'POST'])
def getAdmin(companyId):
    sql = "SELECT * FROM  user WHERE company_id = '" + \
        companyId + "' and company_role = 'Admin';"

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


@ app.route('/getTokenData/<tokenId>', methods=['GET', 'POST'])
def getTokenData(tokenId):
    sql = "SELECT * FROM  tbl_microsoft_tokens WHERE id = '" + \
        tokenId + "' and current_status = 1;"

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


@ app.route('/verifyTokenData', methods=['GET', 'POST'])
def getTokenDataVerify():
    tokenId = request.form.get("tokenId")
    sql = "SELECT t.current_status,u.name FROM  tbl_microsoft_tokens t LEFT JOIN user u ON u.email = t.email WHERE t.accessToken = '" + \
        tokenId + "' and current_status = 1;"
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


@ app.route('/getTokenDataDetails/<tokenId>', methods=['GET', 'POST'])
def getTokenDataDetails(tokenId):
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


@ app.route('/getArtefacts/<projectId>', methods=['GET', 'POST'])
def getArtefacts(projectId):
    sql = "SELECT * FROM  artefact WHERE project_id = '" + projectId + "';"

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


@ app.route('/getArtefact/<artId>', methods=['GET', 'POST'])
def getArtefact(artId):
    sql = "SELECT * FROM  artefact WHERE artefact_id = '" + artId + "';"

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


@ app.route('/getContainer/<contId>', methods=['GET', 'POST'])
def getContainer(contId):
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


@ app.route('/updateContainer/<contTitle>/<contId>', methods=['GET', 'POST'])
def updateContainer(contTitle, contId):
    sql = "UPDATE hierarchy_container SET container_title = '" + str(contTitle) + "' WHERE container_id = '" + str(
        contId) + "';"

    mydb.close()
    mydb.connect()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    # mycursor.close()
    return ({"message": "success"})


@ app.route('/addContainer/<containerName>/<root>/<projId>/<herId>', methods=['GET', 'POST'])
def addContainer(containerName, root, projId, herId):
    print("heirarchyid: " + herId)
    if (root == "root"):
        value = (containerName, projId, herId)
        sql = "INSERT INTO hierarchy_container (container_title, project_id, hierarchy_id) VALUES (%s, %s, %s)"
    if (root != "root"):
        value = (containerName, projId, herId, root)
        sql = "INSERT INTO hierarchy_container (container_title, project_id, hierarchy_id, parent_container_id) VALUES (%s, %s, %s, %s)"

    mydb.close()
    mydb.connect()
    mycursor = mydb.cursor()
    mycursor.execute(sql, value)
    mydb.commit()
    # mycursor.close()
    message = {"message": "success"}
    return jsonify(message)


# @ app.route('/getHeirarchyList/<project_id>', methods=['GET', 'POST'])
# def getHeirarchyList(project_id):
#     # sql = "SELECT h.* FROM  hierarchy_list h LEFT JOIN hierarchy_container c ON c.hierarchy_id = h.hierarchy_id where c.project_id = %s"
#     print("PROJECT ID",project_id)
#     sql = "SELECT * FROM hierarchy_list WHERE project_id=%s;"
#     values=(project_id,)
#     mycursor = mydb.cursor()
#     mycursor.execute(sql,values)
#     result = mycursor.fetchall()
#     print(result)
#     row_headers = [x[0] for x in mycursor.description]
#     result = [dict(zip(row_headers, res)) for res in result]
#     print(result)
#     return jsonify(result)

@ app.route('/getHeirarchyList/<project_id>', methods=['GET', 'POST'])
def getHeirarchyList(project_id):
    sql = "SELECT * FROM hierarchy_list WHERE project_id = %s;"
    values = (project_id,)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql, values)
        result = mycursor.fetchall()
    except Exception as e:
        return jsonify({'error': e, "status": False})
    # row_headers = [x[0] for x in mycursor.description]
    row_headers = ['hierarchy_id', 'hierarchy_name', 'project_id']

    result = [dict(zip(row_headers, res)) for res in result]
    print(result)
    return jsonify({"Data": result, "Status": True})


@ app.route('/getHeirarchyList', methods=['GET', 'POST'])
def getHeirarchyListData():
    sql = "SELECT * FROM hierarchy_list "
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        result = mycursor.fetchall()
    except Exception as e:
        return jsonify({'error': e, "status": False})
    # row_headers = [x[0] for x in mycursor.description]
    row_headers = ['hierarchy_id', 'hierarchy_name', 'project_id']

    result = [dict(zip(row_headers, res)) for res in result]
    print(result)
    return jsonify({"Data": result, "Status": True})


@ app.route('/getContainers/<heirarchyId>/<projId>', methods=['GET', 'POST'])
def getContainers(heirarchyId, projId):
    sql = "SELECT * FROM  hierarchy_container where hierarchy_id = '" + \
        heirarchyId + "' and project_id = '" + projId + "';"

    mydb.close()
    mydb.connect()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    result = mycursor.fetchall()
    row_headers = [x[0] for x in mycursor.description]
    # mycursor.close()
    result = [dict(zip(row_headers, res)) for res in result]
    print(result)
    return jsonify(result)


@ app.route('/moveContainer/<contId>/<type>/<pContId>/<heirarchyId>', methods=['GET', 'POST'])
def moveContainer(contId, type, pContId, heirarchyId):
    if (type == "container"):
        sql = "UPDATE hierarchy_container SET parent_container_id = '" + str(pContId) + "' WHERE container_id = '" + str(
            contId) + "';"

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
        # mycursor.close()
    else:
        sql = "SELECT cal.* FROM  container_artefact_link cal,  hierarchy_container hc WHERE hc.container_id=cal.container_id and hc.hierarchy_id = '" + str(
            heirarchyId) + "' and cal.artefact_id = '" + str(contId) + "';"

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        contLinkInfo = mycursor.fetchall()
        # mycursor.close()
        if (contLinkInfo):
            previousContId = contLinkInfo[0][1]
        else:
            previousContId = ""
        val = (pContId, contId)
        sql = "INSERT INTO container_artefact_link (container_id, artefact_id) VALUES (%s, %s)"

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        mydb.commit()
        # mycursor.close()
        sql = "DELETE FROM  container_artefact_link WHERE artefact_id = '" + str(
            contId) + "' and container_id = '" + str(previousContId) + "';"
        # sql = "UPDATE container_artefact_link SET container_id = '" + str(pContId) + "' WHERE artefact_id = '" + str(
        #   contId) + "';"

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
        # mycursor.close()
    customerId = {"message": "success"}
    return jsonify(customerId)


def copyRecursive(hostId, destId):
    sql = "SELECT a.* FROM  artefact a,  container_artefact_link ca WHERE a.artefact_id = ca.artefact_id and ca.container_id = '" + str(
        hostId) + "';"

    mydb.close()
    mydb.connect()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    artefacts = mycursor.fetchall()
    # mycursor.close()
    for a in artefacts:
        sql = "INSERT INTO artefact (artefact_type, artefact_owner, artefact_name, description, status, create_date, update_date, location_url, template_url, project_id, template) SELECT artefact_type, artefact_owner, artefact_name, description, status, create_date, update_date, location_url, template_url, project_id, template FROM artefact WHERE artefact_id = '" + str(
            a[0]) + "';"

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
        artId = mycursor.lastrowid
        # mycursor.close()
        val = (destId, artId)
        sql = "INSERT INTO container_artefact_link (container_id, artefact_id) VALUES (%s, %s)"

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        mydb.commit()
        # mycursor.close()
    sql = "SELECT * FROM  hierarchy_container where parent_container_id = '" + \
        str(hostId) + "';"

    mydb.close()
    mydb.connect()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    containers = mycursor.fetchall()
    # mycursor.close()
    for c in containers:
        sql = "INSERT INTO hierarchy_container (container_title, project_id, hierarchy_id, parent_container_id) SELECT container_title, project_id, hierarchy_id, '" + str(
            destId) + "' FROM hierarchy_container WHERE container_id = '" + str(c[0]) + "';"

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
        destId = mycursor.lastrowid
        # mycursor.close()
        hostId = c[0]
        copyRecursive(hostId, destId)


@ app.route('/copyContainer/<contId>/<type>/<pContId>', methods=['GET', 'POST'])
def copyContainer(contId, type, pContId):
    if (type == "container"):
        sql = "INSERT INTO hierarchy_container (container_title, project_id, hierarchy_id, parent_container_id) SELECT container_title, project_id, hierarchy_id, '" + str(
            pContId) + "' FROM hierarchy_container WHERE container_id = '" + str(contId) + "';"

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
        destId = mycursor.lastrowid
        # mycursor.close()
        hostId = contId
        copyRecursive(hostId, destId)
    else:
        sql = "INSERT INTO artefact (artefact_type, artefact_owner, artefact_name, description, status, create_date, update_date, location_url, template_url, project_id, template) SELECT artefact_type, artefact_owner, artefact_name, description, status, create_date, update_date, location_url, template_url, project_id, template FROM artefact WHERE artefact_id = '" + str(
            contId) + "';"

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
        artId = mycursor.lastrowid
        # mycursor.close()
        val = (pContId, artId)
        sql = "INSERT INTO container_artefact_link (container_id, artefact_id) VALUES (%s, %s)"

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        mydb.commit()
        # mycursor.close()
    customerId = {"message": "success"}
    return jsonify(customerId)


def deleteRecursive(contId):
    ret = ""
    sql = "SELECT a.* FROM  artefact a,  container_artefact_link ca WHERE a.artefact_id = ca.artefact_id and ca.container_id = '" + str(
        contId) + "';"

    mydb.close()
    mydb.connect()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    artefacts = mycursor.fetchall()
    # mycursor.close()
    if (artefacts):
        return "error"
    # for a in artefacts:
    #   sql = "DELETE FROM  container_artefact_link WHERE artefact_id = '" + str(a[0]) + "';"
    #   mycursor.execute(sql)
    #   mydb.commit()
    #   sql = "DELETE FROM  artefact WHERE artefact_id = '" + str(a[0]) + "';"
    #   mycursor.execute(sql)
    #   mydb.commit()
    sql = "SELECT * FROM  hierarchy_container where parent_container_id = '" + \
        str(contId) + "';"

    mydb.close()
    mydb.connect()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    containers = mycursor.fetchall()
    # mycursor.close()
    if (containers):
        for c in containers:
            ret = deleteRecursive(c[0])
    if (ret == "error"):
        return "error"
    sql = "DELETE FROM  hierarchy_container WHERE container_id = '" + \
        str(contId) + "';"

    mydb.close()
    mydb.connect()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    # mycursor.close()
    return "done"


@ app.route('/deleteContainer/<contId>/<type>', methods=['GET', 'POST'])
def deleteContainer(contId, type):
    if (type == "container"):
        msg = deleteRecursive(contId)
    else:
        sql = "SELECT * FROM  artefact WHERE artefact_id = '" + contId + "';"

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        result = mycursor.fetchall()
        row_headers = [x[0] for x in mycursor.description]
        # mycursor.close()
        document = [dict(zip(row_headers, res)) for res in result]

        # sql = "DELETE cal FROM  container_artefact_link cal,  hierarchy_container hc WHERE hc.container_id=cal.container_id and hc.hierarchy_id = '" + str(heirarchyId) + "' and cal.artefact_id = '" + str(contId) + "';"
        sql = "DELETE FROM  container_artefact_link WHERE artefact_id = '" + \
            str(contId) + "';"

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
        # mycursor.close()
        sql = "DELETE FROM  artefact WHERE artefact_id = '" + \
            str(contId) + "';"

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
        # mycursor.close()
        # print(document)
        print("document path is: " +
              document[0]['location_url'] + '/' + document[0]["artefact_name"] + '.docx')
        if (os.path.exists(document[0]['location_url'] + '/' + document[0]["artefact_name"] + '.docx')):
            print("deleting document")
            os.remove(document[0]['location_url'] + '/' +
                      document[0]["artefact_name"] + '.docx')
        msg = "done"
    customerId = {"message": msg}
    return jsonify(customerId)


def recursive(projId, c):
    sql = "SELECT h.*,p.project_name,c.company_name FROM  hierarchy_container h LEFT JOIN project p ON p.project_id = h.project_id LEFT JOIN company c ON c.company_id = p.company_id WHERE h.project_id = '" + projId + "' and h.parent_container_id = '" + str(
        c) + "';"
    try:
        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        containers = mycursor.fetchall()
    except Exception as e:
        print("Error is",e)
    # mycursor.close()
    jsn = []
    if (containers):
        for cont in containers:
            temp = {}
            childJson = []
            data = {}
            data['id'] = cont[0]
            data['node'] = cont[1]
            data['company_name'] = cont[6]
            data['project_name'] = cont[5]
            data['artefact_type'] = ""
            data['status'] = ""
            data['artefact_owner'] = ""
            temp["data"] = data
            sql = "SELECT a.*,p.project_name,c.company_name FROM  artefact a LEFT JOIN project p ON p.project_id = a.project_id LEFT JOIN company c ON c.company_id = p.company_id,  container_artefact_link ca WHERE a.artefact_id = ca.artefact_id and ca.container_id = '" + str(
                cont[0]) + "';"

            mydb.close()
            mydb.connect()
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            artefacts = mycursor.fetchall()
            # mycursor.close()
            for a in artefacts:
                temp2 = {}
                data = {}
                data['id'] = str(a[0])
                data['node'] = str(a[3])
                data['company_name'] = str(a[13])
                data['project_name'] = str(a[12])
                data['artefact_type'] = str(a[1])
                data['status'] = str(a[5])
                data['artefact_owner'] = str(a[2])
                temp2["data"] = data
                childJson.append(temp2)
            result = recursive(projId, cont[0])
            if (result):
                for r in result:
                    childJson.append(r)
                temp["children"] = childJson
            elif (childJson):
                temp["children"] = childJson
            jsn.append(temp)
        return jsn
    else:
        return jsn


def recursiveTemp(projId, c):
    sql = "SELECT h.*,p.project_name,c.company_name FROM  hierarchy_container h LEFT JOIN project p ON p.project_id = h.project_id LEFT JOIN company c ON c.company_id = p.company_id WHERE  h.parent_container_id = '" + str(
        c) + "';"
    try:
        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        containers = mycursor.fetchall()
    except Exception as e:
        print("My error is >>",e )
    # mycursor.close()
    jsn = []
    if (containers):
        for cont in containers:
            temp = {}
            childJson = []
            data = {}
            data['id'] = cont[0]
            data['node'] = cont[1]
            data['company_name'] = cont[6]
            data['project_name'] = cont[5]
            data['artefact_type'] = ""
            data['status'] = ""
            data['artefact_owner'] = ""
            temp["data"] = data
            sql = "SELECT a.*,p.project_name,c.company_name FROM  artefact a LEFT JOIN project p ON p.project_id = a.project_id LEFT JOIN company c ON c.company_id = p.company_id,  container_artefact_link ca WHERE a.artefact_id = ca.artefact_id and ca.container_id = '" + str(
                cont[0]) + "';"

            mydb.close()
            mydb.connect()
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            artefacts = mycursor.fetchall()
            # mycursor.close()
            for a in artefacts:
                temp2 = {}
                data = {}
                data['id'] = str(a[0])
                data['node'] = str(a[3])
                data['company_name'] = str(a[13])
                data['project_name'] = str(a[12])
                data['artefact_type'] = str(a[1])
                data['status'] = str(a[5])
                data['artefact_owner'] = str(a[2])
                temp2["data"] = data
                childJson.append(temp2)
            result = recursive(projId, cont[0])
            if (result):
                for r in result:
                    childJson.append(r)
                temp["children"] = childJson
            elif (childJson):
                temp["children"] = childJson
            jsn.append(temp)
        return jsn
    else:
        return jsn


@ app.route('/getprojectTree/<projectId>/<heirId>', methods=['GET', 'POST'])
def getprojectTree(projectId, heirId):
    sql = "SELECT a.*,p.project_name,c.company_name FROM  artefact a LEFT JOIN project p ON p.project_id = a.project_id LEFT JOIN company c ON c.company_id = p.company_id WHERE a.project_id = '" + projectId + \
        "' and a.artefact_id NOT IN (SELECT cal.artefact_id FROM  container_artefact_link cal,  hierarchy_container hc where cal.container_id=hc.container_id and hc.hierarchy_id = '" + heirId + "');"

    mydb.close()
    mydb.connect()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    pArtefacts = mycursor.fetchall()

    # mycursor.close()
    sql = "SELECT h.*,p.project_name,c.company_name FROM  hierarchy_container h LEFT JOIN project p ON p.project_id = h.project_id LEFT JOIN company c ON c.company_id = p.company_id WHERE  h.project_id = '" + \
        projectId + "' and h.hierarchy_id = '" + \
        heirId + "' and h.parent_container_id IS NULL;"

    mydb.close()
    mydb.connect()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    pcontainers = mycursor.fetchall()

    # mycursor.close()
    contJson = []
    for idx, pc in enumerate(pcontainers):
        temp = {}
        childJson = []
        data = {}
        data['id'] = pc[0]
        data['node'] = pc[1]
        data['company_name'] = pc[6]
        data['project_name'] = pc[5]
        data['artefact_type'] = ""
        data['status'] = ""
        data['artefact_owner'] = ""
        # data['location_url'] = ""
        temp["data"] = data
        sql = "SELECT a.*,p.project_name,c.company_name FROM  artefact a LEFT JOIN project p ON p.project_id = a.project_id LEFT JOIN company c ON c.company_id = p.company_id,  container_artefact_link ca  WHERE a.artefact_id = ca.artefact_id and ca.container_id = '" + str(
            pc[0]) + "';"
        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        artefacts = mycursor.fetchall()
        # mycursor.close()
        print("HHHHH>>>>>>>>>>SSSSSS", artefacts)
        for a in artefacts:
            temp2 = {}
            data = {}
            data['id'] = str(a[0])
            data['node'] = str(a[3])
            data['company_name'] = str(a[13])
            data['project_name'] = str(a[12])
            data['artefact_type'] = str(a[1])
            data['status'] = str(a[5])
            data['artefact_owner'] = str(a[2])
            data['location_url'] = str(a[8])
            temp2["data"] = data
            childJson.append(temp2)
        result = recursive(projectId, pc[0])
        if (result):
            for r in result:
                childJson.append(r)
            temp["children"] = childJson
        elif (childJson):
            temp["children"] = childJson
        contJson.append(temp)
    print("p artefacts: ")
    print(pArtefacts)
    for pa in pArtefacts:
        tempa = {}
        data = {}
        data['id'] = str(pa[0])
        data['node'] = str(pa[3])
        data['company_name'] = str(pa[13])
        data['project_name'] = str(pa[12])
        data['artefact_type'] = str(pa[1])
        data['status'] = str(pa[5])
        data['artefact_owner'] = str(pa[2])
        data['location_url'] = str(pa[8])
        tempa["data"] = data
        contJson.append(tempa)
    return jsonify(contJson)


# @ app.route('/getprojectTree/<projectId>/<heirId>', methods=['GET', 'POST'])
# def getprojectTree(projectId, heirId):

    
#     sql_company = "select * from company "
#     try:
        
#         mycursor = mydb.cursor()
#         mycursor.execute(sql_company)
#         data_company = mycursor.fetchall()
#     except Exception as e:
#         print(e)
#     if data_company:
#         companyJson = []
#         for d in data_company:
#             print("companyID>>>>>",d[0])
#             temp1 = {}
#             childJson = []
#             data = {}
#             data['id'] = d[0]
#             data['node'] = d[2]
#             data['company_name'] = ''
#             data['project_name'] = ''
#             data['artefact_type'] = ""
#             data['status'] = ""
#             data['artefact_owner'] = ""
#             temp1["data"] = data

#             sql = "select * from project where company_id = ".format(d[0])
#             mydb.close()
#             mydb.connect()
#             mycursor = mydb.cursor()
#             mycursor.execute(sql)
#             projects = mycursor.fetchall()
#             # mycursor.close()
#             print("HHHHH", projects)
#             projectJson = []
#             for p in projects:
#                 childJson = []
#                 temp2 = {}
#                 data = {}
#                 data['id'] = str(p[0])
#                 data['node'] = str(p[2])
#                 data['company_name'] = ''
#                 data['project_name'] = ''
#                 data['artefact_type'] = ''
#                 data['status'] = ''
#                 data['artefact_owner'] = ''
#                 temp2["data"] = data
#                 childJson.append(temp2)

#                 sql = "SELECT a.*,p.project_name,c.company_name FROM  artefact a LEFT JOIN project p ON p.project_id = a.project_id LEFT JOIN company c ON c.company_id = p.company_id WHERE a.project_id = '" + p[0] + \
#         "' and a.artefact_id NOT IN (SELECT cal.artefact_id FROM  container_artefact_link cal,  hierarchy_container hc where cal.container_id=hc.container_id and hc.hierarchy_id = '" + heirId + "');"

#                 mydb.close()
#                 mydb.connect()
#                 mycursor = mydb.cursor()
#                 mycursor.execute(sql)
#                 pArtefacts = mycursor.fetchall()

#                 # mycursor.close()
#                 sql = "SELECT h.*,p.project_name,c.company_name FROM  hierarchy_container h LEFT JOIN project p ON p.project_id = h.project_id LEFT JOIN company c ON c.company_id = p.company_id WHERE  h.project_id = '" + \
#                     p[0] + "' and h.hierarchy_id = '" + \
#                     heirId + "' and h.parent_container_id IS NULL;"

#                 mydb.close()
#                 mydb.connect()
#                 mycursor = mydb.cursor()
#                 mycursor.execute(sql)
#                 pcontainers = mycursor.fetchall()

#                 # mycursor.close()
#                 contJson = []
#                 for idx, pc in enumerate(pcontainers):
#                     temp3 = {}
#                     childJson = []
#                     data = {}
#                     data['id'] = pc[0]
#                     data['node'] = pc[1]
#                     data['company_name'] = pc[6]
#                     data['project_name'] = pc[5]
#                     data['artefact_type'] = ""
#                     data['status'] = ""
#                     data['artefact_owner'] = ""
#                     temp3["data"] = data
#                     sql = "SELECT a.*,p.project_name,c.company_name FROM  artefact a LEFT JOIN project p ON p.project_id = a.project_id LEFT JOIN company c ON c.company_id = p.company_id,  container_artefact_link ca  WHERE a.artefact_id = ca.artefact_id and ca.container_id = '" + str(
#                         pc[0]) + "';"
#                     mydb.close()
#                     mydb.connect()
#                     mycursor = mydb.cursor()
#                     mycursor.execute(sql)
#                     artefacts = mycursor.fetchall()
#                     # mycursor.close()
#                     print("HHHHH", artefacts)
#                     for a in artefacts:
#                         temp2 = {}
#                         data = {}
#                         data['id'] = str(a[0])
#                         data['node'] = str(a[3])
#                         data['company_name'] = str(a[13])
#                         data['project_name'] = str(a[12])
#                         data['artefact_type'] = str(a[1])
#                         data['status'] = str(a[5])
#                         data['artefact_owner'] = str(a[2])
#                         temp2["data"] = data
#                         childJson.append(temp2)
#                     result = recursive(projectId, pc[0])
#                     if (result):
#                         for r in result:
#                             childJson.append(r)
#                         temp["children"] = childJson
#                     elif (childJson):
#                         temp["children"] = childJson
#                     contJson.append(temp)
#                     projectJson.append()
#                 print("p artefacts: ")
#                 print(pArtefacts)
#                 for pa in pArtefacts:
#                     tempa = {}
#                     data = {}
#                     data['id'] = str(pa[0])
#                     data['node'] = str(pa[3])
#                     data['company_name'] = str(pa[13])
#                     data['project_name'] = str(pa[12])
#                     data['artefact_type'] = str(pa[1])
#                     data['status'] = str(pa[5])
#                     data['artefact_owner'] = str(pa[2])
#                     tempa["data"] = data
#                     contJson.append(tempa)
#                 return jsonify(contJson)


def getProjectsTreeData(projectId,heirId):
    sql = "SELECT a.*,p.project_name,c.company_name FROM  artefact a LEFT JOIN project p ON p.project_id = a.project_id LEFT JOIN company c ON c.company_id = p.company_id WHERE a.project_id = '" + projectId + \
        "' and a.artefact_id NOT IN (SELECT cal.artefact_id FROM  container_artefact_link cal,  hierarchy_container hc where cal.container_id=hc.container_id and hc.hierarchy_id = '" + heirId + "');"

    mydb.close()
    mydb.connect()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    pArtefacts = mycursor.fetchall()

    # mycursor.close()
    sql = "SELECT h.*,p.project_name,c.company_name FROM  hierarchy_container h LEFT JOIN project p ON p.project_id = h.project_id LEFT JOIN company c ON c.company_id = p.company_id WHERE  h.project_id = '" + \
        projectId + "' and h.hierarchy_id = '" + \
        heirId + "' and h.parent_container_id IS NULL;"

    mydb.close()
    mydb.connect()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    pcontainers = mycursor.fetchall()

    # mycursor.close()
    contJson = []
    for idx, pc in enumerate(pcontainers):
        temp = {}
        childJson = []
        data = {}
        data['id'] = pc[0]
        data['node'] = pc[1]
        data['company_name'] = pc[6]
        data['project_name'] = pc[5]
        data['artefact_type'] = ""
        data['status'] = ""
        data['artefact_owner'] = ""
        temp["data"] = data
        sql = "SELECT a.*,p.project_name,c.company_name FROM  artefact a LEFT JOIN project p ON p.project_id = a.project_id LEFT JOIN company c ON c.company_id = p.company_id,  container_artefact_link ca  WHERE a.artefact_id = ca.artefact_id and ca.container_id = '" + str(
            pc[0]) + "';"
        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        artefacts = mycursor.fetchall()
        # mycursor.close()
        print("HHHHH", artefacts)
        for a in artefacts:
            temp2 = {}
            data = {}
            data['id'] = str(a[0])
            data['node'] = str(a[3])
            data['company_name'] = str(a[13])
            data['project_name'] = str(a[12])
            data['artefact_type'] = str(a[1])
            data['status'] = str(a[5])
            data['artefact_owner'] = str(a[2])
            temp2["data"] = data
            childJson.append(temp2)
        result = recursive(projectId, pc[0])
        if (result):
            for r in result:
                childJson.append(r)
            temp["children"] = childJson
        elif (childJson):
            temp["children"] = childJson
        contJson.append(temp)
    print("p artefacts: ")
    print(pArtefacts)
    for pa in pArtefacts:
        tempa = {}
        data = {}
        data['id'] = str(pa[0])
        data['node'] = str(pa[3])
        data['company_name'] = str(pa[13])
        data['project_name'] = str(pa[12])
        data['artefact_type'] = str(pa[1])
        data['status'] = str(pa[5])
        data['artefact_owner'] = str(pa[2])
        tempa["data"] = data
        contJson.append(tempa)
    return jsonify(contJson)


# function to generate OTP
def generateOTP():
    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""

    # length of password can be changed
    # by changing value in range
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP


@ app.route('/emailVerification/<email>', methods=['GET', 'POST'])
def emailVerification(email):
    OTP = str(generateOTP())
    msg = "your OTP is " + OTP
    # msg = "hi"
    port = 465
    password = "@Mushi123"
    # Create a secure SSL context
    # ssl._create_default_https_context = ssl._create_unverified_context
    context = ssl._create_unverified_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("rapidpm.musab@gmail.com", password)
        server.sendmail("rapidpm.musab@gmail.com", email, msg)
    customerId = {"message": str(OTP)}
    return jsonify(customerId)


@ app.route("/projects",  methods=['GET', 'POST'])
def post_projects():

    company_id = request.form.get('company_id')
    project_id = request.form.get('project_id')
    artefact_type = request.form.get('artefact_type')
    # print("before get_projects")

    where = ""

    if company_id != "":
        if where != "":
            where += ' AND (c.RPM = "Yes" OR p.company_id = {}) '.format(company_id)
        else:
            where += ' (c.RPM = "Yes" OR p.company_id = {}) '.format(company_id)

    if project_id != "":
        if where != "":
            where += ' AND a.project_id = {} '.format(project_id)
        else:
            where += ' a.project_id = {} '.format(project_id)

    if artefact_type != "":
        if where != "":
            where += ' AND a.artefact_type =   "{}" '.format(artefact_type)
        else:
            where += ' a.artefact_type =  "{}" '.format(artefact_type)

    sub_query = " SELECT p.project_id,p.project_name,c.company_name FROM `artefact` a INNER JOIN project p ON p.project_id = a.project_id INNER JOIN company c ON c.company_id = p.company_id "

    if where != '':
        sub_query += " WHERE " + where + " "

    sub_query += " group by a.project_id "
    print(sub_query)
    try:

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sub_query)
    except (mydb.Error, mydb.Warning) as e:
        print(e)

    data = mycursor.fetchall()
    # mycursor.close()
    output_list = []
    for sublist in data:
        project_dict = {}
        project_dict["project_id"] = sublist[0]
        project_dict["project_name"] = sublist[1]
        project_dict["company_name"] = sublist[2]
        output_list.append(project_dict)

    return jsonify(output_list)


@ app.route('/getContainerstemplateselection/<project_id>/<company_id>', methods=['GET', 'POST'])
def getContainersTemplateSelection(project_id, company_id):

    where = " p.template = 'Y' "

    # if project_id != "":
    #     if where != "":
    #         where += ' AND h.project_id = {}  '.format(project_id)
    #     else:
    #         where += ' h.project_id = {} '.format(project_id)

    if company_id != "":
        if where != "":
            where += " AND (c.RPM = 'Yes' OR p.company_id = {})  ".format(company_id)
        else:
            where += ' (c.RPM = "Yes" OR p.company_id = {})  '.format(company_id)

    sub_query = "SELECT h.* FROM `hierarchy_container` h  INNER JOIN project p ON p.project_id = h.project_id  INNER JOIN company c ON c.company_id = p.company_id"
    if where != "":
        sub_query += " WHERE " + where + " "

    print("My query --->>> ", sub_query)
    try:
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sub_query)
    except (mydb.Error, mydb.Warning) as e:
        print(e)

    result = mycursor.fetchall()
    print("result", result)
    row_headers = [x[0] for x in mycursor.description]
    result = [dict(zip(row_headers, res)) for res in result]
    print(result)
    return jsonify(result)


@ app.route('/getprojectTrees/<project_id>/<company_id>/<artefact_type>', methods=['GET', 'POST'])
def getprojectTrees(project_id, company_id, artefact_type):

    where = " a.template = 'Y' "

    if artefact_type != "22":
        if where != "":
            where += " AND (c.RPM = 'Yes' OR a.artefact_type = '{}')  ".format(artefact_type)
        else:
            where += " (c.RPM = 'Yes' OR a.atrefact_type = '{}')  ".format(artefact_type)

    if company_id != "":
        if where != "":
            where += " AND (c.RPM = 'Yes' OR p.company_id = {})  ".format(company_id)
        else:
            where += " (c.RPM = 'Yes' OR p.company_id = {})  ".format(company_id)

    sub_query = "SELECT a.*,p.project_name,c.company_name FROM artefact a LEFT JOIN project p ON p.project_id = a.project_id LEFT JOIN company c ON c.company_id = p.company_id "
    end_query = "AND (a.artefact_id NOT IN (SELECT cal.artefact_id FROM container_artefact_link cal,  hierarchy_container hc where cal.container_id=hc.container_id) OR c.RPM = 'Yes');"

    if where != "":
        sub_query += " WHERE " + where + " "
    sub_query += end_query
    try:
        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sub_query)
        pArtefacts = mycursor.fetchall()
    except (mydb.Error, mydb.Warning) as e:
        print(e)
    sql = "SELECT h.*,p.project_name,c.company_name FROM hierarchy_container h LEFT JOIN project p ON p.project_id = h.project_id LEFT JOIN company c ON c.company_id = p.company_id  WHERE p.template='Y'  and h.parent_container_id IS NULL;"

    try:
        mycursor.execute(sql)
        pContainers = mycursor.fetchall()
    except (mydb.Error, mydb.Warning) as e:
        print(e)
    contJson = []
    for idx, pc in enumerate(pContainers):
        temp = {}
        childJson = []
        data = {}
        data['id'] = pc[0]
        data['node'] = pc[1]
        data['company_name'] = pc[6]
        data['project_name'] = pc[5]
        data['artefact_type'] = ""
        data['status'] = ""
        data['artefact_owner'] = ""
        temp["data"] = data

        whr = " p.template = 'Y' "
        # if project_id:
        #     if whr != "":
        #         whr += " AND  h.project_id = {} ".format(project_id)
        #     else:
        #         whr += " h.project_id = {} ".format(project_id)
        if company_id != '':
            if whr != "":
                whr += " AND (c.RPM = 'Yes' OR p.company_id = {})  ".format(company_id)
            else:
                whr += " (c.RPM = 'Yes' OR p.company_id = {}) ".format(company_id)

        sub_query = " SELECT h.*,p.project_name,c.company_name FROM `hierarchy_container` h LEFT JOIN project p ON p.project_id = h.project_id LEFT JOIN company c ON c.company_id = p.company_id "
        if whr != "":
            sub_query += " WHERE "+whr+" ;"
        mycursor.execute(sub_query)
        artefacts = mycursor.fetchall()
        # mycursor.close()
        for a in artefacts:
            temp2 = {}
            data = {}
            data['id'] = str(a[0])
            data['node'] = str(a[3])
            data['company_name'] = str(a[6])
            data['project_name'] = str(a[5])
            data['artefact_type'] = str(a[1])
            data['status'] = str(a[4])
            data['artefact_owner'] = str(a[2])
            temp2["data"] = data
            childJson.append(temp2)
        result = recursiveTemp(project_id, pc[0])
        if (result):
            for r in result:
                childJson.append(r)
            temp["children"] = childJson
        elif (childJson):
            temp["children"] = childJson
        contJson.append(temp)
    for pa in pArtefacts:
        tempa = {}
        data = {}
        data['id'] = str(pa[0])
        data['node'] = str(pa[3])
        data['company_name'] = str(pa[13])
        data['project_name'] = str(pa[12])
        data['artefact_type'] = str(pa[1])
        data['status'] = str(pa[5])
        data['artefact_owner'] = str(pa[2])
        tempa["data"] = data
        contJson.append(tempa)
        print("contJson",contJson)
    return jsonify(contJson)

@ app.route('/getArtefactData/<companyId>', methods=['GET', 'POST'])
def getArtefactData(companyId):
    sql = 'SELECT c.company_id, c.company_name,a.*, cal.container_id, hc.parent_container_id,p.project_name,hc.container_title  FROM artefact a JOIN project p ON a.project_id = p.project_id JOIN company c ON p.company_id = c.company_id LEFT JOIN container_artefact_link cal ON cal.artefact_id = a.artefact_id LEFT JOIN hierarchy_container hc ON hc.container_id = cal.container_id AND hc.project_id = p.project_id AND hc.hierarchy_id = p.hierarchy_id_default WHERE a.template = "Y" AND (c.company_id = {} OR c.RPM = "Yes") ORDER BY c.company_name ASC;'.format(companyId)
    try:
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        result = mycursor.fetchall()
        row_headers = [x[0] for x in mycursor.description]
        result = [dict(zip(row_headers, res)) for res in result]
        print("MY RESULT>>>>",result)
        contJson = []

        for item in result:
            contJson.append({'data': {
                'id': item['artefact_id'],
                'artefact_name': item['artefact_name'],
                'company_name': item['company_name'],
                'project_name': item['project_name'],
                'artefact_type': item['artefact_type'],
                'status': item['status'],
                'artefact_owner': item['artefact_owner']
            }})

        print(contJson)
        return jsonify ({'status':True,'msg':'Artefact Data Fetch','data':contJson})
    except Exception as e:
        print("ERROR in getArtefactData ",e)
        return jsonify ({'status':False,'msg':e})

@ app.route("/company_list",  methods=['GET', 'POST'])
def company_list():

    sql = " SELECT company_name, RPM, company_id FROM `company`; "

    try:

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
    except (mydb.Error, mydb.Warning) as e:
        print(e)
    data = mycursor.fetchall()
    mycursor.close()
    output_list = []
    for sublist in data:
        project_dict = {}
        project_dict["company_name"] = sublist[0]
        project_dict["RPM"] = sublist[1]
        project_dict["company_id"] = sublist[2]
        output_list.append(project_dict)

    return jsonify(output_list)


@ app.route("/type_id_list/<project_id>",  methods=['GET', 'POST'])
def type_id_list(project_id):

    where = ""
    # if project_id != "":
    #     where += " where project_id = {}".format(project_id)
    sql = " SELECT artefact_type FROM artefact_type_default " + where + " ; "
    print("syntax ", sql)
    try:

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
    except (mydb.Error, mydb.Warning) as e:
        print(e)
    data = mycursor.fetchall()
    mycursor.close()
    print("My data xxxxxxx ", data)
    output_list = []
    for sublist in data:
        print(sublist)
        project_dict = {}
        project_dict["artefact_type"] = sublist[0]
        output_list.append(project_dict)
        # project_dict["project_id"] = sublist[0]
    return jsonify(output_list)


@ app.route("/getArtifactDetailsData/<artifactId>",  methods=['GET', 'POST'])
def getArtifactDetailsData(artifactId):

    sql = " SELECT * FROM artefact WHERE artefact_id = {} ".format(artifactId)
    print("syntax ", sql)
    try:

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
    except (mydb.Error, mydb.Warning) as e:
        print(e)
    result = mycursor.fetchall()
    row_headers = [x[0] for x in mycursor.description]
    result = [dict(zip(row_headers, res)) for res in result]
    return jsonify(result)


@ app.route("/project_detail/<company_id>",  methods=['GET', 'POST'])
def project_details(company_id):
    where = ''
    if company_id != '':
        where = ' or company_id = {}'.format(company_id)

    sql = "SELECT project_name, project_id FROM project WHERE company_id = 1 " + where + ";"
    print("QUERY --->>>>", sql)

    try:

        mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
    except (mydb.Error, mydb.Warning) as e:
        print(e)
    data = mycursor.fetchall()
    mycursor.close()
    print("My data xxxxxxx ", data)
    output_list = []
    for sublist in data:
        project_dict = {}
        project_dict["project_name"] = sublist[0]
        project_dict["project_id"] = sublist[1]
        output_list.append(project_dict)

    return jsonify(output_list)


@ app.route("/update_artefact_data",  methods=['POST'])
def update_artefact_data():
    if request.method == 'POST':
        artefact = request.form['artInfo']
        artefact = json.loads(artefact)
        print("Artefact Dictionary Data",artefact)
        if 'location_url' in artefact and 'template_url' in artefact:
            print(1)
            sql_statement = "UPDATE artefact SET artefact_type = '" + str(artefact['artefact_type']) + "', artefact_owner = '" + str(
                artefact['artefact_owner']) + "', artefact_name = '" + str(artefact['artefact_name']) + "', description = '" + \
                            str(artefact['description']) + "', status = '" + str(artefact['status']) + "',create_date = '" + str(
                artefact['create_date']) + "',update_date = '" + str(artefact['update_date']) + "',location_url = '" + str(
                artefact['location_url']) + "',template_url = '" + str(artefact['template_url']) + "',project_id = '" + str(
                artefact['project_id']) + "',template = '" + str(artefact['template']) + "' WHERE artefact_id = '" + str(
                artefact['artefact_id']) + "';"
        else:
            print(2)
            sql_statement = "UPDATE artefact SET artefact_type = '" + str(artefact[
                'artefact_type']) + "', artefact_owner = '" + str(
                artefact['artefact_owner']) + "', artefact_name = '" + str(artefact['artefact_name']) + "', description = '" + \
                str(artefact['description']) + "', status = '" + str(artefact['status']) + "',create_date = '" + str(
                artefact[
                    'create_date']) + "',update_date = '" + str(artefact['update_date']) + "',project_id = '" + str(
                artefact['project_id']) + "',template = '" + str(artefact['template']) + "' WHERE artefact_id = '" + str(
                artefact['artefact_id']) + "';"
        # print(sql_staement)
        try:
            mydb.close()
            mydb.connect()
            mycursor = mydb.cursor()
            mycursor.execute(sql_statement)
            mydb.commit()
            return jsonify({'status': True})
        except (mydb.Error, mydb.Warning) as e:
            print(e)
            return jsonify({'status': False})


@ app.route("/insert_artefact_data",  methods=['POST'])
def insert_artefact_data():
    if request.method == 'POST':
        artefact_type = request.form.get('artefact_type')
        artefact_owner = request.form.get('artefact_owner')
        artefact_name = request.form.get('artefact_name')
        description = request.form.get('description')
        status = request.form.get('status')
        location_url = request.form.get('location_url')
        template_url = request.form.get('template_url')
        project_id = request.form.get('project_id')
        template = request.form.get('template')
        container_id = request.form.get('container_id')
       
        create_date = date.today()
        update_date = date.today()
        if location_url == "":
            # sql_staement = "SELECT location_url FROM `artefact_type_default` WHERE project_id = {} and artefact_type = '{}';".format(
            #     project_id, artefact_type)
            sql_staement = "SELECT location_url FROM `artefact_type_default` WHERE artefact_type = '{}';".format(
                artefact_type)
            try:
                mydb.close()
                mydb.connect()
                mycursor = mydb.cursor()
                mycursor.execute(sql_staement)
            except (mydb.Error, mydb.Warning) as e:
                print(e)
            location_url_data = mycursor.fetchall()
            if location_url_data:
                location_url = location_url_data[0][0]
                print("location_url", location_url)
            else:
                location_url = ""

    sql = "INSERT INTO artefact (artefact_type, artefact_owner, artefact_name, description, status, create_date, update_date, location_url, template_url,project_id,template) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
        artefact_type, artefact_owner, artefact_name, description, status, create_date, update_date, location_url, template_url, project_id, template)
    print(sql)
    try:
        # mydb.close()
        mydb.connect()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        mydb.commit()
        if container_id != "root":
            sql = "SELECT LAST_INSERT_ID()"
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            artefact_id = {"message": str(
                mycursor.fetchall()[0]).split('(')[1].split(',')[0]}
            sql = "INSERT INTO container_artefact_link (container_id, artefact_id) VALUES ('{}', '{}');".format(
                container_id, artefact_id["message"])
            # mydb.close()
            mydb.connect()
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            mydb.commit()
        return jsonify({'status': True})
    except (mydb.Error, mydb.Warning) as e:
        print(e)
        return jsonify({'status': False})


def companyArtefact(project_id):
    
    sql = "SELECT ca.artefact_type FROM project p JOIN company_artefact_types ca ON p.company_id = ca.company_id WHERE p.project_id = {};".format(project_id)
    try:
        mycursor.execute(sql)
        data = mycursor.fetchall()
        print("Company Artefact Data",data[0][0])
        return data[0][0]
    except (mydb.Error, mydb.Warning) as e:
        print(e)
    
@ app.route("/content_screen",  methods=['GET', 'POST'])
def contentSelectionScreen():
    project_id = request.form.get('project_id')
    artefact_id = request.form.get('artefact_id')
    artefact_owner = request.form.get('owner')
    print("ARTEFACT OWNER---->>",artefact_owner)
    # artefact_type = request.form.get('artefact_type')
    # artefact_type = 'pid'
    id_tupple = tuple(json.loads(artefact_id))
    if len(id_tupple) == 1:
        id_tupple = str(id_tupple).replace(",", " ")
    print('ID TUPPLE',id_tupple)
    sql = " SELECT * FROM `artefact` WHERE artefact_id IN {}; ".format(
        id_tupple)
    print("Content Selection Screen", sql)
    try:
        mycursor.execute(sql)
        data = mycursor.fetchall()
    except (mydb.Error, mydb.Warning) as e:
        print(e)
    
    print("data contentSelectionScreen", data)

    new_data = []
    for d in data:
        sql_staement = "SELECT location_url FROM `artefact_type_default` WHERE project_id = {} and artefact_type = '{}';".format(
            project_id, d[1])
        print("SQL STATEMENT>>>", sql_staement)
        try:
            mycursor.execute(sql_staement)
        except (mydb.Error, mydb.Warning) as e:
            print(e)
        location_url_data = mycursor.fetchall()
        if location_url_data:
            location_url = location_url_data[0][0]
            print("location_url", location_url)
        else:
            location_url = ""
        d = (d[0], d[1], d[2], d[3], d[4], d[5],
             d[6], d[7], location_url, d[8], 1, d[11])
        new_data.append(d)
    print("new data", new_data)
    artefact_type_data = companyArtefact(project_id)
    print("artefact_type_data",artefact_type_data)
    for d in new_data:
        artefact_id = d[0]
        artefact_type = artefact_type_data
        # artefact_owner = d[2]
        artefact_owner = artefact_owner
        artefact_name = d[3]
        description = d[4]
        status = d[5]
        create_date = date.today()
        update_date = date.today()
        location_url
        template_url = d[9]
        project_id
        template = d[11]
        sql_query = "INSERT INTO artefact (artefact_type, artefact_owner, artefact_name, description, status, create_date, update_date, location_url, template_url,project_id,template) VALUES  ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(
            artefact_type, artefact_owner, artefact_name, description, status, create_date, update_date, location_url, template_url, project_id, template)
        print(sql_query)
        try:
            mycursor.execute(sql_query)
            mydb.commit()
            # pass
        except (mydb.Error, mydb.Warning) as e:
            print(e)
            return jsonify({'status': False})
    print(new_data)
    return jsonify({'status': True})


@app.route("/insert_user_data",  methods=['POST'])
def insertUser():

    if request.method == 'POST':
        company_name = request.form.get('company_name')
        contact_name = request.form.get('contact_name')
        address_line1 = request.form.get('address_line1')
        address_line2 = request.form.get('address_line2')
        address_line3 = request.form.get('address_line3')
        user_id = request.form.get('user_id')

    sql = "INSERT INTO company (company_name,contact_name,address_line1,address_line2,address_line3,RPM) VALUES (%s, %s, %s, %s, %s,%s)"
    values = (company_name, contact_name, address_line1,
              address_line2, address_line3, 'No')
    print(sql)
    print("Values--->>>", values)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql, values)
        mydb.commit()
    except Exception as e:
        print("Error", e)

    sql = "SELECT LAST_INSERT_ID()"
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        companyId = {"message": str(
            mycursor.fetchall()[0]).split('(')[1].split(',')[0]}
    except Exception as e:
        print("Error ", e)
    sql = "INSERT INTO user_company_role (company_id,company_role,user_id) VALUES (%s, %s, %s)"
    values_user = (companyId["message"], "Admin", user_id)
    try:
        mycursor.execute(sql, values_user)
        mydb.commit()
    except Exception as e:
        print("Error ", e)

    return jsonify({'status': True})


def send_email(msg,email):
    # Create a message object
    message = Message('', sender='rapidPMV2@outlook.com', recipients=[email])

    # Set the content of the message
    reset_url = f"http://82.69.10.205:4200"
    html_content = f'''
            <html>
            <body>
                <p>{msg}</p>
                <p>Please click on the link <a href="{reset_url}">Here</a> to  access this shared company.</p>
                
            </body>
            </html>
        '''
    message = MIMEMultipart("alternative")
    message["Subject"] = "New Company Added"
    message["From"] = "rapidPMV2@outlook.com"
    message["To"] = email
    message.attach(MIMEText(html_content, "html"))

    # Send email using smtplib
    smtp_server = 'smtp.office365.com'
    sender_email = "rapidPMV2@outlook.com"
    sender_password = "Alchemist21@#"

    

    # message = f"Subject: Password Reset\n\n"
    # message += f"Click the following link to reset your password:\n"
    # message += f"{reset_url}"

    try:
        with smtplib.SMTP(smtp_server, 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
            return True
    except Exception as e:
        print("An error occurred while sending the email:", str(e))
        return False


    # Send the message
    # mail.send(message)

    

def reset_password_request_members(email,msg):
    print("Requesting password reset")
    

    if not email:
        return jsonify({"status": False, "msg": "Email is required."}), 400

    # Find the user by email in the database
    select_query = "SELECT user_id FROM user WHERE email = %s"
    select_values = (email,)

    try:
        mycursor = mydb.cursor()
        mycursor.execute(select_query, select_values)
        user_id = mycursor.fetchone()[0]
        mycursor.close()
        print("USER ID ____>>>>", user_id)
    except Exception as e:
        print("An error occurred while reset_password_request", e)

    if not user_id:
        return jsonify({"status": False, "msg": "User not found."})

    # Generate and store password reset token
    token = generate_password_reset_token(user_id)

    # Send password reset email to the user
    flag = 1
    status = send_password_reset_email(email, token,flag,msg)
    return status
    # if status:
    #     return jsonify({"status": True, "msg": "Password reset instructions sent to your email."})

    # return jsonify({"status": False, "msg": "Eror! Password reset"})




@app.route("/insert_user_data_info",  methods=['POST'])
def insertUserData():
    result = False
    if request.method == 'POST':
        company_id = request.form.get('company_id')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        print("Enter email", email)
        company_role = 'user'
        status = 'Pending'
       

    sql = "select company_name from company where company_id = %s"
    sql_val = (company_id,)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql, sql_val)
        company_name = mycursor.fetchone()[0]
    except Exception as e:
        print("Error in",e)


  
    sql = "SELECT email,user_id FROM user WHERE email = %s; "
    value = (email,)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql, value)
        result = mycursor.fetchall()[0]
        # print("My result", result)
    except Exception as e:
        print("Error ", e)

    # email exist in database then send email notfication that you are added in this company 
    if result:
        msg = 'you have been setup in RapidPM by {} for company {}'.format(email,company_name)
        mail_send = send_email(msg,email)
        if mail_send:
            sql = "INSERT INTO user_company_role (company_id,user_id,company_role) VALUES (%s, %s, %s)"
            values_user = (company_id, result[1], company_role)
            try:
                mycursor = mydb.cursor()
                mycursor.execute(sql, values_user)
                mydb.commit()
                return jsonify ({'status':True,'message':"User Data Inserted Succesffully"})
            except Exception as e:
                print("Error ", e)
                return jsonify({'error':e,'status':False})

    # user is not in database 
    else:
        msg = 'you have been setup in RapidPM by {} for company {}.'.format(email,company_name)
        
        sql = "INSERT INTO user (name,email,company_role,status, company_id,verified,password,firstLogin) VALUES (%s, %s, %s, %s, %s,%s,%s,%s)"
        values_user = (name, email, company_role, status,
                    company_id, 'Pending', password,'N')

        try:

            mycursor = mydb.cursor()
            mycursor.execute(sql, values_user)
            mydb.commit()

            sql_insertedId = "SELECT LAST_INSERT_ID() as id "
            mycursor = mydb.cursor()
            mycursor.execute(sql_insertedId)
            insertId = {"message": str(
                mycursor.fetchall()[0]).split('(')[1].split(',')[0]}

            sql = "INSERT INTO user_company_role (company_id,user_id,company_role) VALUES (%s, %s, %s)"
            values_user = (company_id, insertId["message"], company_role)
            mycursor = mydb.cursor()
            mycursor.execute(sql, values_user)
            mydb.commit()
        except Exception as e:
            print("Error ", e)

        status = reset_password_request_members(email,msg)

        if status:
            print("Into Update")
            sql = "UPDATE user SET status = %s, verified = %s, firstLogin = %s  WHERE email = %s;"
            val_user = ("verified", "Y", "Y", email)
            try:
                mycursor = mydb.cursor()
                mycursor.execute(sql, val_user)
                mydb.commit()
            except Exception as e:
                print("Error in Confirm update query", e)

        # return jsonify({'msg': 'Your account has been successfully verified. You can now log in.', 'status': True})
   

            return jsonify({'status': True})

@app.route("/update_user_data_info",  methods=['POST'])
def updateUserData():
    result = False
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        name = request.form.get('name')
        email = request.form.get('email')
        print("Enter email", email)
        company_role = 'user'
        status = request.form.get('status')

    sql = "SELECT email FROM user WHERE email = %s AND user_id != %s "
    value = (email, user_id)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql, value)
        result = mycursor.fetchall()
        print("My result", result)
    except Exception as e:
        print("Error ", e)

    if result:
        print("Email Already exist")
        return jsonify({"status": False, "msg": "Email Already Exists"})

    else:
        sql = "UPDATE user SET name=%s,email=%s,company_role=%s,status=%s,verified=%s,firstLogin=%s WHERE user_id = %s"
        values_user = (name, email, company_role,
                       status, 'Y', 'Y', user_id)

        try:
            mycursor = mydb.cursor()
            mycursor.execute(sql, values_user)
            mydb.commit()
            # print(mycursor.statement)
            return jsonify({'status': True})
        except Exception as e:
            print("Error ", e)
            return jsonify({'status': False})


@app.route("/update_user_data",  methods=['POST'])
def updateUser():

    if request.method == 'POST':
        company_name = request.form.get('company_name')
        contact_name = request.form.get('contact_name')
        address_line1 = request.form.get('address_line1')
        address_line2 = request.form.get('address_line2')
        address_line3 = request.form.get('address_line3')
        company_id = request.form.get('company_id')
        user_id = request.form.get('user_id')

    sql = "UPDATE company SET company_name = %s,contact_name=%s,address_line1=%s,address_line2=%s,address_line3=%s WHERE company_id=%s "
    values = (company_name, contact_name, address_line1,
              address_line2, address_line3, company_id)
    print(sql)
    print("Values--->>>", values)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql, values)
        mydb.commit()
    except Exception as e:
        print("Error", e)
    return jsonify({'status': True})


@app.route("/auth_process",  methods=['POST'])
def authenticationProcess():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
    sql = " SELECT email FROM user where email= %s"
    val_email = (email,)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql, val_email)
        email_result = mycursor.fetchall()
        print(email_result)
    except Exception as e:
        print("Error is ", e)

    if email_result:
        sql = " SELECT password from user where email = %s"
        try:
            mycursor = mydb.cursor()
            mycursor.execute(sql, val_email)
            password_result_db = mycursor.fetchall()[0][0]
            print(password_result_db)
        except Exception as e:
            print("Error is ", e)
        if password_result_db == password:
            jwt_string = jwtToken(email, password)
            current_status = 0
            sql = "UPDATE tbl_microsoft_tokens SET current_status = {} WHERE email = '{}';".format(
                current_status, email)
            # status = 0
            # value = (status,email)
            print("My first ", sql)
            try:
                mycursor = mydb.cursor()
                mycursor.execute(sql)
                mydb.commit()
            except Exception as e:
                print("Error in Update query 1 ", e)

            sql = "INSERT INTO tbl_microsoft_tokens (accessToken,idToken,email,isAuthenticated, current_status,name) VALUES (%s, %s, %s, %s, %s,%s)"
            val_microsoft_table = (jwt_string, jwt_string, email, 1, 1, "")
            try:
                mycursor = mydb.cursor()
                mycursor.execute(sql, val_microsoft_table)
                # insertId = mycursor.lastrowid
                mydb.commit()
            except Exception as e:
                print("Error in Insert Query ", e)
            sql_insertedId = "SELECT LAST_INSERT_ID() as id "
            try:
                mycursor = mydb.cursor()
                mycursor.execute(sql_insertedId)
                insertId = {"message": str(
                    mycursor.fetchall()[0]).split('(')[1].split(',')[0]}
                # insertId = mycursor.fetchall()[0][0]
                print("Insert", insertId)
                return jsonify({'status': True, 'tokenId': insertId['message'], 'msg': "Success", "type": "SIGNIN"})
            except Exception as e:
                print("Error in query 3.1", e)
        else:
            return jsonify({'status': False, 'tokenId': "", 'msg': "Incorrect password"})
    else:
        jwt_string = jwtToken(email, password)
        current_status = 0
        sql = "UPDATE tbl_microsoft_tokens SET current_status = {} WHERE email = '{}';".format(
            current_status, email)
        # print(sql)
        # status = int(0)
        # value = (status,email)
        try:
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            mydb.commit()
        except Exception as e:
            print("Error in Update query2 ", e)

        sql = "INSERT INTO tbl_microsoft_tokens (accessToken,idToken,email,isAuthenticated, current_status,name) VALUES (%s, %s, %s, %s, %s,%s)"
        val_microsoft_table = (jwt_string, jwt_string, email, 1, 1, "")
        try:
            mycursor = mydb.cursor()
            mycursor.execute(sql, val_microsoft_table)
            mydb.commit()
            # insertId = mycursor.lastrowid
            # return jsonify({'status':'True','tokenId':insertId,'msg':"Success","type":"SIGNUP"})
        except Exception as e:
            print("Error in Insert Query ", e)
        sql_insertedId = "SELECT LAST_INSERT_ID() as id "
        try:
            mycursor = mydb.cursor()
            mycursor.execute(sql_insertedId)
            insertId = {"message": str(
                mycursor.fetchall()[0]).split('(')[1].split(',')[0]}
            # insertId = mycursor.fetchall()[0][0]
            print("Insert", insertId)
            return jsonify({'status': True, 'tokenId': insertId['message'], 'msg': "Success", "type": "SIGNUP"})
        except Exception as e:
            print("Error in query 3.1", e)

# Create account page


@app.route("/signin", methods=['POST'])
def loginAccount():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form.get('email')
        password = request.form.get('password')
    sql = " SELECT * FROM user where email= %s"
    print(sql)
    val_email = (email,)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql, val_email)
        result = mycursor.fetchall()[0]
        print("Email db email: ", result)
    except Exception as e:
        print("Error in createAccount", e)
    db_password = result[2]
    if db_password:
        # proceed with authentication process
        if db_password == password:
            # set session variables and redirect to dashboard
            # authenticationProcess(email, password)
            print("Inside db_password")
            sql = "UPDATE user SET firstLogin = %s where email=%s;"
            val_user = ("Y", result[1])
            try:
                mycursor = mydb.cursor()
                mycursor.execute(sql, val_user)
                mydb.commit()
            except Exception as e:
                print("Error in Confirm update query", e)

        else:
            # display error message
            error = 'Incorrect password. Please try again.'
            return jsonify({'msg': error})
    else:
        # display error message
        error = 'This account does not exist.'
        return jsonify({'msg': error})
    return jsonify({'msg': "successfull Login"})


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        print("email", email, password)

        # validate email
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            error = 'Please enter a valid email address.'
            return jsonify({'msg': error})
        else:
            # check if email already exists in database
            user = ""
            sql = "SELECT * FROM user WHERE email = %s"
            val_email = (email,)
            try:
                mycursor = mydb.cursor()
                mycursor.execute(sql, val_email)
                user = mycursor.fetchone()
                print("my user: -->>>", user)
            except Exception as e:
                print("Error in createAccount", e)

            if user:
                # display error message
                if user[6] == "Y":
                    error = 'This email address is already in use. Please use a different email address or log in.'
                    return jsonify({'msg': error, 'status': False})
                else:
                    if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&*]{8,}$', password):
                        error = 'Your password must meet the following requirements: 8 characters in length, at least one uppercase letter, one lowercase letter, one numeric digit, one special character, and no white spaces.'
                        return jsonify({"msg": error, 'status': False})
                    else:

                        # EMAIL VERIFICATION
                        print("Your password I am here")

                        token = s.dumps(email, salt='email-confirmation-key')
                        print("token:", token)
                        # subject = "Account Verification - Rapid PM"
                        msg = Message("Account Verification - Rapid PM",
                                      sender='rapidPMV2@outlook.com', recipients=[email])
                        # print("msg is --->>> ",msg)
                        # link = url_for(
                        #     'http://localhost:35557/app-email-verify-screen/', token=token, _external=True)
                        link = 'http://82.69.10.205:4200/app-email-verify-screen/'+token
                        # link = BASE_URL + '/confirm/' + token
                        print("link is --->>> ", link)
                        msg.body = """
                                Hello {mailid},
                                Thank you for registering with Rapid PM. To complete the account creation process, please click the link below to verify your email address. This link is valid for 1 hour.

                                {url}

                                If you did not request this email or if the link has expired, please ignore this message
                                and request a new verification email from our website.


                                Best regards,
                                Rapid PM Team
                                """ .format(mailid=email, url=link)
                        print(" message body is --->>> ", msg.body)
                        mail.send(msg)
                        print(" After mail send--->>> ")
                        sql = " UPDATE user SET token = %s WHERE email = %s"
                        print(sql)
                        val_user = (token, email)
                        try:
                            mycursor = mydb.cursor()
                            mycursor.execute(sql, val_user)
                            mydb.commit()
                        except Exception as e:
                            print("Error in Update query for user", e)
                            return jsonify({'msg': 'false', 'status': False})
                        return jsonify({'msg': "A validation email has been sent to your email address. Please check your inbox and follow the instructions to verify your account. This email is valid for 1 hour.", 'status': True})
            else:
                # validate password
                if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
                    error = 'Your password must meet the following requirements: 8 characters in length, at least one uppercase letter, one lowercase letter, one numeric digit, one special character, and no white spaces.'
                    return jsonify({"msg": error, 'status': False})
                else:

                    # EMAIL VERIFICATION
                    print("Your password I am here")

                    token = s.dumps(email, salt='email-confirmation-key')
                    print("token:", token)
                    # subject = "Account Verification - Rapid PM"
                    msg = Message("Account Verification - Rapid PM",
                                  sender='rapidPMV2@outlook.com', recipients=[email])
                    # print("msg is --->>> ",msg)
                    # link = url_for('http://localhost:35557/app-email-verify-screen/', token=token, _external=True)
                    link = 'http://82.69.10.205:4200/app-email-verify-screen/'+token
                    # link = BASE_URL + '/confirm/' + token
                    print("link is --->>> ", link)
                    msg.body = """
                            Hello {mailid},
                            Thank you for registering with Rapid PM. To complete the account creation process, please click the link below to verify your email address. This link is valid for 1 hour.

                            {url}

                            If you did not request this email or if the link has expired, please ignore this message
                            and request a new verification email from our website.


                            Best regards,
                            Rapid PM Team
                            """ .format(mailid=email, url=link)
                    print(" message body is --->>> ", msg.body)
                    mail.send(msg)
                    print(" After mail send--->>> ")
                    sql = "INSERT INTO user (email,password,status,verified,firstLogin,token) VALUES (%s, %s, %s, %s, %s,%s)"
                    print(sql)
                    print(email, password, "Pending", "N", "N", token)
                    val_user = (email, password, "Pending", "N", "N", token)
                    try:
                        mycursor = mydb.cursor()
                        mycursor.execute(sql, val_user)
                        mydb.commit()
                    except Exception as e:
                        print("Error in Insert query for user", e)
                        return jsonify({'msg': 'false', 'status': False})
                    return jsonify({'msg': "A validation email has been sent to your email address. Please check your inbox and follow the instructions to verify your account. This email is valid for 1 hour.", 'status': True})


@app.route('/confirm/<token>')
def confirm(token):

    try:
        email = s.loads(token, salt='email-confirmation-key', max_age=180)
        print(email)
        sql = "UPDATE user SET status = %s, verified = %s  WHERE token = %s;"
        val_user = ("verified", "Y", token)
        try:
            mycursor = mydb.cursor()
            mycursor.execute(sql, val_user)
            mydb.commit()
        except Exception as e:
            print("Error in Confirm update query", e)

        return jsonify({'msg': 'Your account has been successfully verified. You can now log in.', 'status': True})
    except Exception as e:
        print("Error in confirmation", e)
        return jsonify({'msg': "Error in confirmation, clicked after link expired", 'status': False})


@app.route('/artefact_type_detail/<company_id>', methods=['GET', 'POST'])
def getArtefactTypeDetail(company_id):

    sql = "SELECT d.artefact_type,d.type_id FROM `artefact_type_default` d;"
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        result = mycursor.fetchall()
        print("Result-->>,result")
        if result:
            return jsonify({'msg': result})
        else:
            return jsonify({'msg': "No Data Found "})
    except Exception as e:
        print("Error in Artefact Type Detail", e)
        return e


@app.route('/artefact_type_detail_data/<project_id>', methods=['GET', 'POST'])
def getArtefactTypeDetailData(project_id):

    sql = "SELECT c.artefact_type,p.id FROM project_artefact_type_defaults p LEFT JOIN company_artefact_types c ON c.id = p.artefact_type LEFT JOIN company cm ON cm.company_id = c.company_id WHERE (cm.RPM = 'Yes' OR p.project_id = %s);"
    try:
        mydb.connect()
        mycursor = mydb.cursor()
        val_user = (project_id,)
        mycursor.execute(sql, val_user)
        result = mycursor.fetchall()
        # print("Result-->>,result", result)
        if result:
            return jsonify({'msg': result})
        else:
            return jsonify({'msg': "No Data Found "})
    except Exception as e:
        print("Error in Artefact Type Detail", e)
        return e


@app.route('/artefact_status/<company_id>', methods=['GET', 'POST'])
def getArtefactStatus(company_id):

    sql = "SELECT DISTINCT a.status FROM `artefact` a INNER JOIN project p ON p.project_id = a.project_id INNER JOIN company c ON c.company_id = p.company_id WHERE c.RPM = 'Yes' OR c.company_id = %s;"
    val_artefact_status = (company_id,)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql, val_artefact_status)
        result = mycursor.fetchall()
        print("Result-->>,result")
        if result:
            return jsonify({'msg': result})
        else:
            return jsonify({'msg': "No Data Found "})
    except Exception as e:
        return jsonify({'msg': "No Data Found "})


@app.route('/artefact_owner/<company_id>', methods=['GET', 'POST'])
def getArtefactOwner(company_id):

    sql = "SELECT DISTINCT a.artefact_owner FROM `artefact` a INNER JOIN project p ON p.project_id = a.project_id INNER JOIN company c ON c.company_id = p.company_id WHERE c.RPM = 'Yes' OR c.company_id = %s;"
    val_artefact_owner = (company_id,)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql, val_artefact_owner)
        result = mycursor.fetchall()
        print("Result-->>,result")
        if result:
            return jsonify({'msg': result})
        else:
            return jsonify({'msg': "No Data Found "})
    except Exception as e:
        print("Error in Artefact Status", e)


@app.route('/deleteuser/<user_id>', methods=['GET', 'POST'])
def deleteUser(user_id):

    sql = "select user_id from user where user_id = %s;"
    val_user = (user_id,)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql, val_user)
        user = mycursor.fetchone()
        if not user:
            return jsonify({'status': False, "message": "No User found"})

    except Exception as e:
        print("Error", e)

    sql = "select user_id from user_company_role  where user_id = %s;"

    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql, val_user)
        user = mycursor.fetchone()
        print("my user: -->>>", user)
        if not user:
            try:
                print("Deleting user")
                sql = "DELETE FROM user WHERE user_id = %s"
                print("SQL: ", sql)
                mycursor = mydb.cursor()
                mycursor.execute(sql, val_user)
                mydb.commit()
                return jsonify({'status': True, 'message': 'User has been deleted'})
            except Exception as e:
                print("Error: ", e)
        else:
            return jsonify({'status': False, 'message': 'User has registered a company ...Delete Company First'})
    except Exception as e:
        print("Error in deleting user", e)


@app.route('/deleteproject/<project_id>', methods=['GET', 'POST'])
def deleteProject(project_id):

    sql = "select project_id from  hierarchy_container where project_id = %s;"
    val_project = (project_id,)
    print("-->>>", val_project)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql, val_project)
        project = mycursor.fetchone()
        print("my company: -->>>", project)
        if not project:
            try:
                print("Deleting Project")
                sql = "DELETE FROM project WHERE project_id = %s"
                print("SQL: ", sql)
                mycursor = mydb.cursor()
                mycursor.execute(sql, val_project)
                mydb.commit()
                return jsonify({'status': True, 'message': 'Project has been deleted'})
            except Exception as e:
                print("Error: ", e)
        else:
            return jsonify({'status': False, 'message': 'Project has Container ...Delete Container First'})
    except Exception as e:
        print("Error in deleting project", e)
        return jsonify({'status': False})


@app.route('/deletecompany/<company_id>', methods=['GET', 'POST'])
def deleteCompany(company_id):

    sql = "select company_id from project where company_id = %s;"
    val_company = (company_id,)
    print("-->>>", val_company)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql, val_company)
        company = mycursor.fetchone()
        print("my company: -->>>", company)
        if not company:
            try:
                print("Soft Deleting Company")
                sql = "UPDATE company SET is_deleted = 1 WHERE company_id = %s;"
                print("SQL: ", sql)
                mycursor = mydb.cursor()
                mycursor.execute(sql, val_company)
                mydb.commit()
                return jsonify({'status': True, 'message': 'Company has been deleted'})
            except Exception as e:
                print("Error: ", e)
                return jsonify({'status': False})
        else:
            return jsonify({'status': False, 'message': 'Company has registered project ...Delete Project First'})
    except Exception as e:
        print("Error in deleting company", e)
        return jsonify({'status': False})


# Generate and store password reset token in the database
def generate_password_reset_token(user_id):
    # Generate a secure random token
    token = secrets.token_hex(16)
    print("Generating password reset token", token)
    # Store the token in the database along with user_id and expiration time
    insert_query = "INSERT INTO password_reset (token, user_id) VALUES (%s, %s)"
    values = (token, user_id)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(insert_query, values)
        mydb.commit()
        return token
    except Exception as e:
        print("Error in generate_password_reset_token ", e)

# Send password reset email to the user


def send_password_reset_email(email, token,flag,msg):
    # Construct the reset password URL using the token
    reset_url = f"http://82.69.10.205:4200/app-reset-password-update/{token}"
    # reset_url = url_for('Reset', token=token, _external=True)
    if flag:
        html_content = f'''
            <html>
            <body>
                <p>{msg}</p>
                <p>Please click on the link <a href="{reset_url}">Here</a> to set your password and access this shared company.</p>
                
            </body>
            </html>
        '''
    else:
        html_content = f'''
            <html>
            <body>
                <p>Click the following link to reset your password:</p>
                <a href="{reset_url}">Here</a>
            </body>
            </html>
        ''' 
    # Create the email message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset"
    message["From"] = "rapidPMV2@outlook.com"
    message["To"] = email
    message.attach(MIMEText(html_content, "html"))

    # Send email using smtplib
    smtp_server = 'smtp.office365.com'
    sender_email = "rapidPMV2@outlook.com"
    sender_password = "Alchemist21@#"

    

    # message = f"Subject: Password Reset\n\n"
    # message += f"Click the following link to reset your password:\n"
    # message += f"{reset_url}"

    try:
        with smtplib.SMTP(smtp_server, 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
            return True
    except Exception as e:
        print("An error occurred while sending the email:", str(e))
        return False

# API endpoint to initiate password reset


@app.route('/reset-password', methods=['POST'])
def reset_password_request():
    print("Requesting password reset")
    email = request.form.get("email")

    if not email:
        return jsonify({"status": False, "msg": "Email is required."}), 400

    # Find the user by email in the database
    select_query = "SELECT user_id FROM user WHERE email = %s"
    select_values = (email,)

    try:
        mycursor = mydb.cursor()
        mycursor.execute(select_query, select_values)
        user_id = mycursor.fetchone()[0]
        mycursor.close()
        print("USER ID ____>>>>", user_id)
    except Exception as e:
        print("An error occurred while reset_password_request", e)

    if not user_id:
        return jsonify({"status": False, "msg": "User not found."})

    # Generate and store password reset token
    token = generate_password_reset_token(user_id)

    # Send password reset email to the user
    status = send_password_reset_email(email, token,flag,msg)
    if status:
        return jsonify({"status": True, "msg": "Password reset instructions sent to your email."})

    return jsonify({"status": False, "msg": "Eror! Password reset"})

# API endpoint to handle password reset


@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):

    print("Password reset")
    # Verify the token's validity and expiration time
    select_query = "SELECT user_id FROM password_reset WHERE token = %s"
    select_values = (token,)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(select_query, select_values)
        user_id = mycursor.fetchone()[0]
        print("USER_ID: ", user_id)
    except Exception as e:
        print("An error occurred while reset_password", e)
        return jsonify({"status": False, "msg": "Invalid or expired token."})

    if not user_id:
        return jsonify({"status": False, "msg": "Invalid or expired token."})

   # Find the user by the user_id in the database
    select_query = "SELECT * FROM user WHERE user_id = %s"
    select_values = (user_id,)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(select_query, select_values)
        user_id = mycursor.fetchone()[0]
        mydb.commit()
        print("USER_ID:<><><>", user_id)
    except Exception as e:
        print("Error while updating passowrd")
        return jsonify({"status": False, "msg": "Invalid or expired token."})

    # Update the user's password in the database
    new_password = request.form.get("new_password")
    if not new_password:
        return jsonify({"msg": "New password is required.", 'status': False})

    if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', new_password):
        error = 'Your password must meet the following requirements: 8 characters in length, at least one uppercase letter, one lowercase letter, one numeric digit, one special character, and no white spaces.'
        return jsonify({"msg": error, 'status': False})

    update_query = "UPDATE user SET password = %s WHERE user_id = %s"
    update_values = (new_password, user_id)

    try:
        mycursor = mydb.cursor()
        mycursor.execute(update_query, update_values)
        mydb.commit()
    except Exception as e:
        print("Error while updating passowrd")
        return jsonify({"status": False, "msg": "Invalid or expired token."})

    # Remove the used token from the database
    delete_query = "DELETE FROM password_reset WHERE token = %s"
    delete_value = (token,)

    try:
        mycursor = mydb.cursor()
        mycursor.execute(delete_query, delete_value)
        mydb.commit()
        print("Successfully deleted Token")
    except Exception as e:
        print("Error while making token NULL ", e)
        return jsonify({"status": False, "msg": "Invalid or expired token."})

    return jsonify({"msg": "Password reset successful.", 'status': True})


################# Reset Password Token #################


@ app.route('/list_company_artefact_types/<company_id>', methods=['GET', 'POST'])
def listCompanyArtefactType(company_id):

    keys = ['id', 'company_id', 'artefact_type', 'description']
    sql = " SELECT * FROM company_artefact_types WHERE company_id = %s; "
    list_value = (company_id,)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql, list_value)
        data_list = mycursor.fetchall()
        print("My Data", data_list)
        dictionary_data = [{key: value for key,
                            value in zip(keys, item)} for item in data_list]
        print("RESULT>>>", dictionary_data)
        return jsonify({'status': True, "msg": "Success", "data": dictionary_data})
    except Exception as e:
        print("My error in listCompanyArtefactType", e)
        return jsonify({"error": e, "status": False})


@ app.route('/insert_company_artefact_types/<company_id>', methods=['GET', 'POST'])
def insertCompanyArtefactType(company_id):

    insert_query = "INSERT INTO company_artefact_types (company_id, artefact_type,description) VALUES (%s, %s,%s)"
    insert_value = (company_id, "", "")
    try:
        mycursor = mydb.cursor()
        mycursor.execute(insert_query, insert_value)
        mydb.commit()
        return jsonify({"status": True, "msg": "Company Artefact Type Data Added"})
    except Exception as e:
        print("My error in insertCompanyArtefactType", e)
        return jsonify({"error": e, "status": False})

    return jsonify({"status": False, "msg": "Duplicate Entry Not Allowed"})


@ app.route('/update_company_artefact_types', methods=['GET', 'POST'])
def updateCompanyArtefactType():

    if request.method == 'POST':
        id_ = request.form.get('id')
        company_id = request.form.get('company_id')
        artefact_type = request.form.get('artefact_type')
        description = request.form.get('description')

    update_query = "UPDATE company_artefact_types SET artefact_type = %s, description = %s WHERE id = %s;"
    update_value = (artefact_type, description, id_)

    try:
        mycursor = mydb.cursor()
        mycursor.execute(update_query, update_value)
        mydb.commit()
        return jsonify({"status": True, "msg": "Company Artefact Type Data Updated"})
    except Exception as e:
        print("Error updating updateCompanyArtefactType", e)
        return jsonify({"error": e, "status": False})


@ app.route('/delete_company_artefact_types/<row_id>', methods=['GET', 'POST'])
def deleteCompanyArtefactType(row_id):

    delete_query = " DELETE FROM company_artefact_types WHERE id = %s "
    delete_value = (row_id,)

    try:
        mycursor = mydb.cursor()
        mycursor.execute(delete_query, delete_value)
        mydb.commit()
        return jsonify({"status": True, "msg": "Company Artefact Type Data Deleted"})
    except Exception as e:
        print("Error updating updateCompanyArtefactType", e)
        return jsonify({"error": e, "status": False})


@ app.route('/list_project_artefact_type_defaults/<project_id>', methods=['GET', 'POST'])
def listProjectArtefactTypeDefaults(project_id):

    keys = ['project_id', 'artefact_type', 'description',
            'default_url', 'template_url', 'multiples', 'mandatory', 'id', 'c_id']
    sql = " SELECT p.project_id,c.artefact_type,c.description,p.default_url,p.template_url,p.multiples,p.mandatory,p.id,c.id as c_id FROM project_artefact_type_defaults p LEFT JOIN company_artefact_types c ON c.id = p.artefact_type WHERE p.project_id = %s; "
    list_value = (project_id,)
    print("SQL STATEMENT", sql)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(sql, list_value)
        data_list = mycursor.fetchall()
        print("My Data", data_list)
        dictionary_data = [{key: value for key,
                            value in zip(keys, item)} for item in data_list]
        print("RESULT>>>", dictionary_data)
        return jsonify({'status': True, "msg": "success", "data": dictionary_data})
    except Exception as e:
        print("My error in listProjectArtefactType", e)
        return jsonify({"error": e, "status": False})


@ app.route('/insert_project_artefact_type_defaults/<project_id>', methods=['GET', 'POST'])
def insertProjectArtefactTypeDefaults(project_id):

    insert_query = "INSERT INTO project_artefact_type_defaults (project_id, artefact_type,description,default_url,template_url,multiples,mandatory) VALUES (%s, %s,%s,%s,%s,%s,%s);"
    insert_value = (project_id, "", "", "", "","1","1")
    try:
        mycursor = mydb.cursor()
        mycursor.execute(insert_query, insert_value)
        mydb.commit()
        return jsonify({"status": True, "msg": "Project Artefact Type Data Added"})
    except Exception as e:
        print("My error in Project Artefact Type", e)
        return jsonify({"error": e, "status": False})


@ app.route('/update_project_artefact_type_defaults', methods=['GET', 'POST'])
def updateProjectArtefactTypeDefaults():

    if request.method == 'POST':
        id_ = request.form.get('id')
        project_id = request.form.get('project_id')
        artefact_type = request.form.get('artefact_type')
        description = request.form.get('description')
        default_url = request.form.get('default_url')
        template_url = request.form.get('template_url')
        multiples = request.form.get('multiples')
        mandatory = request.form.get('mandatory')

    update_query = "UPDATE  project_artefact_type_defaults SET artefact_type = %s, description = %s, default_url = %s,template_url = %s, multiples = %s,mandatory = %s WHERE id = %s;"
    update_value = (artefact_type, description, default_url,
                    template_url, multiples, mandatory, id_)
    # print("update query>>>>>>>>>", update_query)
    try:
        mycursor = mydb.cursor()
        mycursor.execute(update_query, update_value)
        mydb.commit()
        return jsonify({"status": True, "msg": "Project Artefact Type Default Data Updated"})
    except Exception as e:
        print("Error updating updateProjectArtefactTypeDefaults", e)
        return jsonify({"error": e, "status": False})


@ app.route('/delete_project_artefact_types/<id_>', methods=['GET', 'POST'])
def deleteProjectArtefactTypeDefaults(id_):
    delete_query = " DELETE FROM project_artefact_type_defaults WHERE id = %s ;"
    delete_value = (id_,)

    try:
        mycursor = mydb.cursor()
        mycursor.execute(delete_query, delete_value)
        mydb.commit()
        return jsonify({"status": True, "msg": "Project Artefact Type Default Data Deleted"})
    except Exception as e:
        print("Error updating updateProjectArtefactTypeDefaults", e)
        return jsonify({"error": e, "status": False})


@ app.route('/get_company_artefact/<company_id>', methods=['GET', 'POST'])
def getCompanyArtefact(company_id):
    keys = ('id', 'company_id', 'artefact_type', 'description')
    select_query = "SELECT * FROM company_artefact_types WHERE company_id = %s"
    select_value = (company_id,)
    try:
        mycursor.execute(select_query, select_value)
        data_list = mycursor.fetchall()
        print("My Data", data_list)
        dictionary_data = [{key: value for key,
                            value in zip(keys, item)} for item in data_list]
        print("RESULT>>>", dictionary_data)
        return jsonify({'status': True, 'data': dictionary_data})
    except Exception as e:
        print("My error in Project Artefact Type", e)
        return jsonify({"error": e, "status": False})


@ app.route('/get_company_artefact_type_default/<project_id>', methods=['GET', 'POST'])
def getCompanyArtefactTypeDefault(project_id):
    keys = ['id', 'artefact_type']
    sql = "SELECT p.id,c.artefact_type FROM project_artefact_type_defaults p LEFT JOIN company_artefact_types c ON p.artefact_type = c.id WHERE p.project_id = %s"
    values = (project_id,)
    try:
        mycursor.execute(sql, values)
        data_list = mycursor.fetchall()
        print("My Data", data_list)
        dictionary_data = [{key: value for key,
                            value in zip(keys, item)} for item in data_list]
        print("RESULT>>>", dictionary_data)
        return jsonify({'status': True, 'data': dictionary_data})
    except Exception as e:
        print("My error in Project Artefact Type", e)
        return jsonify({"error": e, "status": False})


@ app.route('/get_my_data/<company_id>', methods=['GET', 'POST'])
def getMyData(company_id):
    
    sql = """SELECT c.company_id, a.*, cal.container_id, hc.parent_container_id
            FROM artefact a
            JOIN project p ON a.project_id = p.project_id
            JOIN company c ON p.company_id = c.company_id
            LEFT JOIN container_artefact_link cal ON cal.artefact_id = a.artefact_id
            LEFT JOIN hierarchy_container hc ON hc.container_id = cal.container_id 
            AND hc.project_id = p.project_id AND hc.hierarchy_id = p.hierarchy_id_default
            WHERE a.template = "Y" AND (c.company_id = {} OR c.RPM = "Yes") ORDER BY company_name ASC;""".format(company_id)

    try:
        mycursor.execute(sql)
        data = mycursor.fetchall()
        row_headers = [x[0] for x in mycursor.description]

        print("My Data List",data)
        
    except Exception as e:
        print("My Error is ",e)
    data_dict = [dict(zip(row_headers, res)) for res in data]
    return data_dict
    

