import time

import mysql.connector
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
import json
import pandas as pd
app = Flask(__name__)
# api = Api(app)
CORS(app)

#### MySQL #######3
# initializing database connection
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="musab",
  password="RAPIDPM",
  database = "RPMnew_dataBase",
  auth_plugin='mysql_native_password'
)

# defining cursor to navigate through database
mycursor = mydb.cursor()

#### functions #####
def checkLogin(userEmail,userPassword):
  query = "SELECT cu.password, co.RPM, co.company_id, cu.user_id, cu.company_role FROM user cu, company co WHERE cu.email = '" + userEmail + "' and cu.company_id = co.company_id;"
  mycursor.execute(query)
  result = mycursor.fetchall()
  json_data = []
  if(result):
    print(result)
    if(result[0][0] == userPassword):
      if(result[0][1] != "Yes"):
        json_data.append(dict(zip(["message"], ["Welcome"])))
        json_data.append(dict(zip(["id"], [result[0][3]])))
        json_data.append(dict(zip(["role"], [result[0][4]])))
      else:
        json_data.append(dict(zip(["message"], ["Welcome RPM"])))
        json_data.append(dict(zip(["id"], [result[0][2]])))
        json_data.append(dict(zip(["role"], [result[0][4]])))
    else:
      json_data.append(dict(zip(["message"], ["Incorrect password"])))
  else:
    json_data.append(dict(zip(["message"], ["Email address not found"])))
  return json.dumps(json_data)

@app.route('/login/<userEmail>/<userPassword>', methods=['GET', 'POST'])
def login(userEmail,userPassword):
  ret = checkLogin(userEmail,userPassword)
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
    sql = "INSERT INTO company (" + ", ".join(key) + ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, value)
    mydb.commit()
    sql = "SELECT LAST_INSERT_ID()"
    mycursor.execute(sql)
    companyId = {"message": str(mycursor.fetchall()[0]).split('(')[1].split(',')[0]}
    return jsonify(companyId)
  else:
    sql = "UPDATE company SET RPM = '" + value[0] + "', company_name = '" + value[1] + "', contact_name = '" + value[2] + "', address_line1 = '" + value[
      3] + "', address_line2 = '" + value[4] + "', address_line3 = '" + value[5] + "', city = '" + value[6] + "',country = '" + \
          value[7] + "',postal_code = '" + value[8] + "' WHERE company_id = '" + str(compId) + "';"
    # sql = "UPDATE user SET (" + ", ".join(key) + ") VALUES (%s, %s, %s, %s, %s, %s, %s) WHERE user_id = '" + str(custmId) + "';"
    mycursor.execute(sql)
    mydb.commit()
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
  if(custmId == ""):
    sql = "INSERT INTO user (" + ", ".join(key) + ") VALUES (%s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, value)
    mydb.commit()
    sql = "SELECT LAST_INSERT_ID()"
    mycursor.execute(sql)
    customerId = {"message": str(mycursor.fetchall()[0]).split('(')[1].split(',')[0]}
    return jsonify(customerId)
  else:
    sql = "UPDATE user SET company_id = '" + customer['company_id'] + "', company_role = '" + customer['company_role'] + "', email = '" + customer['email'] + "', name = '" + customer['name'] + "', password = '" + customer['password'] + "', status = '" + customer['status'] + "',verified = '" + customer['verified'] +  "' WHERE user_id = '" + str(custmId) + "';"
    # sql = "UPDATE user SET (" + ", ".join(key) + ") VALUES (%s, %s, %s, %s, %s, %s, %s) WHERE user_id = '" + str(custmId) + "';"
    mycursor.execute(sql)
    mydb.commit()
    customerId = {"message": str(custmId)}
    return jsonify(customerId)

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
    sql = "INSERT INTO project (" + ", ".join(key) + ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, value)
    mydb.commit()
    sql = "SELECT LAST_INSERT_ID()"
    mycursor.execute(sql)
    projectId = {"message": str(mycursor.fetchall()[0]).split('(')[1].split(',')[0]}
    return jsonify(projectId)
  else:
    sql = "UPDATE project SET project_name = '" + str(project[
      'project_name']) + "', template = '" + str(project['template']) + "', status = '" + str(project['status']) + "', owner = '" + \
          str(project['owner']) + "', start = '" + str(project['start']) + "',end = '" + str(project[
            'end']) + "',hierarchy_id_default = '" + str(project['hierarchy_id_default']) + "' WHERE project_id = '" + str(projId) + "';"
    # sql = "UPDATE user SET (" + ", ".join(key) + ") VALUES (%s, %s, %s, %s, %s, %s, %s) WHERE user_id = '" + str(custmId) + "';"
    mycursor.execute(sql)
    mydb.commit()
    customerId = {"message": str(projId)}
    return jsonify(customerId)

@app.route('/getUsers/<company_id>', methods=['GET', 'POST'])
def getUsers(company_id):
  sql = "SELECT * FROM RPMnew_dataBase.user WHERE company_id = '" + company_id + "';"
  mycursor.execute(sql)
  result = mycursor.fetchall()
  header = mycursor.description
  # print(header)
  row_headers = [x[0] for x in mycursor.description]
  # print(row_headers)
  result = [dict(zip(row_headers, res)) for res in result]
  # users = {"message": result};
  print(result)
  return jsonify(result)

@app.route('/getUser/<user_id>', methods=['GET', 'POST'])
def getUser(user_id):
  sql = "SELECT * FROM RPMnew_dataBase.user WHERE user_id = '" + user_id + "';"
  mycursor.execute(sql)
  result = mycursor.fetchall()
  header = mycursor.description
  # print(header)
  row_headers = [x[0] for x in mycursor.description]
  # print(row_headers)
  result = [dict(zip(row_headers, res)) for res in result]
  # users = {"message": result};
  print(result)
  return jsonify(result)

@app.route('/getprojects/<company_id>', methods=['GET', 'POST'])
def getprojects(company_id):
  sql = "SELECT * FROM RPMnew_dataBase.project WHERE company_id = '" + company_id + "';"
  mycursor.execute(sql)
  result = mycursor.fetchall()
  print(result)
  header = mycursor.description
  # print(header)
  row_headers = [x[0] for x in mycursor.description]
  # print(row_headers)
  result = [dict(zip(row_headers, res)) for res in result]
  # users = {"message": result};
  print(result)
  return jsonify(result)

@app.route('/getCompanies', methods=['GET', 'POST'])
def getCompanies():
  sql = "SELECT * FROM RPMnew_dataBase.company;"
  mycursor.execute(sql)
  result = mycursor.fetchall()
  header = mycursor.description
  # print(header)
  row_headers = [x[0] for x in mycursor.description]
  # print(row_headers)
  result = [dict(zip(row_headers, res)) for res in result]
  # users = {"message": result};
  print(result)
  return jsonify(result)

@app.route('/deleteUser/<user_id>', methods=['GET', 'POST'])
def deleteUser(user_id):
  sql = "DELETE FROM user WHERE user_id = '" + user_id + "';"
  mycursor.execute(sql)
  mydb.commit()
  return ({"message":"success"})

@app.route('/deleteProject/<project_id>', methods=['GET', 'POST'])
def deleteProject(project_id):
  sql = "DELETE FROM project WHERE project_id = '" + project_id + "';"
  mycursor.execute(sql)
  mydb.commit()
  return ({"message":"success"})

@app.route('/getCompany/<companyId>', methods=['GET', 'POST'])
def getCompany(companyId):
  sql = "SELECT * FROM RPMnew_dataBase.company WHERE company_id = '" + companyId + "';"
  mycursor.execute(sql)
  result = mycursor.fetchall()
  header = mycursor.description
  # print(header)
  row_headers = [x[0] for x in mycursor.description]
  # print(row_headers)
  result = [dict(zip(row_headers, res)) for res in result]
  # users = {"message": result};
  print(result)
  return jsonify(result)

@app.route('/getProject/<projectId>', methods=['GET', 'POST'])
def getProject(projectId):
  sql = "SELECT * FROM RPMnew_dataBase.project WHERE project_id = '" + projectId + "';"
  mycursor.execute(sql)
  result = mycursor.fetchall()
  header = mycursor.description
  # print(header)
  row_headers = [x[0] for x in mycursor.description]
  # print(row_headers)
  result = [dict(zip(row_headers, res)) for res in result]
  # users = {"message": result};
  print(result)
  return jsonify(result)

@app.route('/getAdmin/<companyId>', methods=['GET', 'POST'])
def getAdmin(companyId):
  sql = "SELECT * FROM RPMnew_dataBase.user WHERE company_id = '" + companyId + "' and company_role = 'Admin';"
  mycursor.execute(sql)
  result = mycursor.fetchall()
  header = mycursor.description
  # print(header)
  row_headers = [x[0] for x in mycursor.description]
  # print(row_headers)
  result = [dict(zip(row_headers, res)) for res in result]
  # users = {"message": result};
  print(result)
  return jsonify(result)

@app.route('/getArtefacts/<projectId>', methods=['GET', 'POST'])
def getArtefacts(projectId):
  sql = "SELECT * FROM RPMnew_dataBase.artefact WHERE project_id = '" + projectId + "';"
  mycursor.execute(sql)
  result = mycursor.fetchall()
  header = mycursor.description
  # print(header)
  row_headers = [x[0] for x in mycursor.description]
  # print(row_headers)
  result = [dict(zip(row_headers, res)) for res in result]
  # users = {"message": result};
  print(result)
  return jsonify(result)

# @app.route('/getprojectTree/<customerId>', methods=['GET', 'POST'])
# def getprojectTree(customerId):
#   sql = "SELECT * FROM RPMnew_dataBase.project WHERE user_id = '" + customerId + "';"
#   mycursor.execute(sql)
#   project = mycursor.fetchall()
#   projJson = []
#   for p in project:
#     temp = {}
#     data = {}
#     data["1"] = p[0]
#     data["2"] = p[1]
#     data["3"] = p[2]
#     data["4"] = p[3]
#     data["5"] = p[4]
#     data["6"] = p[5]
#     data["7"] = p[6]
#     data["8"] = p[7]
#     data["node"] = "project"
#     temp["data"] = data
#     sql = "SELECT * FROM RPMnew_dataBase.stages WHERE project_id = '" + str(p[0]) + "';"
#     mycursor.execute(sql)
#     stages = mycursor.fetchall()
#     stgJson = []
#     for s in stages:
#       temp2 = {}
#       data = {}
#       data['1'] = str(s[0])
#       data['2'] = str(s[1])
#       data['3'] = str(s[2])
#       data['4'] = str(s[3])
#       data['5'] = str(s[4])
#       data['6'] = str(s[5])
#       data['7'] = str(s[6])
#       data["node"] = "stage"
#       temp2["data"] = data
#
#       sql = "SELECT * FROM RPMnew_dataBase.artefact WHERE stage_id = '" + str(s[0]) + "';"
#       mycursor.execute(sql)
#       artefacts = mycursor.fetchall()
#       artJson = []
#       for a in artefacts:
#         temp3 = {}
#         data = {}
#         data['1'] = str(a[0])
#         data['2'] = str(a[1])
#         data['3'] = str(a[2])
#         data['4'] = str(a[3])
#         data['5'] = str(a[4])
#         data['6'] = str(a[5])
#         data['7'] = str(a[6])
#         data['8'] = str(a[7])
#         data["node"] = "artifact"
#
#         temp3["data"] = data
#         artJson.append(temp3)
#       temp2["children"] = artJson
#       stgJson.append(temp2)
#     temp["children"] = stgJson
#     projJson.append(temp)
#   print(projJson)
#   return jsonify(projJson)
def recursive(projId,c):
  sql = "SELECT * FROM RPMnew_dataBase.hierarchy_container WHERE project_id = '" + projId + "' and parent_container_id = '" + str(c) + "';"
  mycursor.execute(sql)
  containers = mycursor.fetchall()
  jsn = []
  if(containers):
    for cont in containers:
      temp = {}
      childJson = []
      data = {}
      data['node'] = cont[1]
      temp["data"] = data
      sql = "SELECT a.* FROM RPMnew_dataBase.artefact a, RPMnew_dataBase.container_artefact_link ca WHERE a.artefact_id = ca.artefact_id and ca.container_id = '" + str(cont[0]) + "';"
      mycursor.execute(sql)
      artefacts = mycursor.fetchall()
      for a in artefacts:
        temp2 = {}
        data = {}
        data['node'] = str(a[2])
        temp2["data"] = data
        childJson.append(temp2)
      result = recursive(projId,cont[0])
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

@app.route('/getprojectTree/<projectId>', methods=['GET', 'POST'])
def getprojectTree(projectId):
  sql = "SELECT * FROM RPMnew_dataBase.hierarchy_container WHERE project_id = '" + projectId + "' and parent_container_id IS NULL;"
  mycursor.execute(sql)
  pcontainers = mycursor.fetchall()
  contJson = []
  for idx, pc in enumerate(pcontainers):
    temp = {}
    childJson = []
    data = {}
    data['node'] = pc[1]
    temp["data"] = data
    sql = "SELECT a.* FROM RPMnew_dataBase.artefact a, RPMnew_dataBase.container_artefact_link ca WHERE a.artefact_id = ca.artefact_id and ca.container_id = '" + str(pc[0]) + "';"
    mycursor.execute(sql)
    artefacts = mycursor.fetchall()
    for a in artefacts:
      temp2 = {}
      data = {}
      data['node'] = str(a[2])
      temp2["data"] = data
      childJson.append(temp2)
    result = recursive(projectId, pc[0])
    if(result):
      for r in result:
        childJson.append(r)
      temp["children"] = childJson
    elif(childJson):
      temp["children"] = childJson
    contJson.append(temp)
  return jsonify(contJson)

app.run(host='0.0.0.0', port=5002, debug=True)
