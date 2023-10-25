from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify

from serverNew import check_url


class Project(ClientAccess):
    def post(self):
        project = request.json
        print("Project from post>>>>>",project)

        if project['location_url'] == 'N':
            project['location_url'] = project['custom_location_url']
            del project['custom_location_url']

        if project['location_url'] != "*RPM":
            res = check_url(project['location_url'])
            print("MY response>>>>>",res)
            if res != True:
                return jsonify ({"status":False,"message":"Invalid URL"})

        projId = project['project_id']
        del project['project_id']

        # if project['custom_location_url']:
        
        
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
                ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)"
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
            os.makedirs("/home/samresh/Documents/RPM/rpm_web_angular_python/artefacts/" +
                        str(project['company_id']) + '/' + str(projectId["message"]), exist_ok=True)
            return jsonify(projectId)
        else:
            sql = "UPDATE project SET project_name = %s, template = %s, status = %s, owner = %s, start = %s, end = %s, hierarchy_id_default = %s, location_url = %s WHERE project_id = %s"
            values = (project['project_name'],project['template'],project['status'],project['owner'],project['start'],project['end'],project['hierarchy_id_default'],project['location_url'],projId)
            try:
                mydb.close()
                mydb.connect()
                mycursor = mydb.cursor()
                mycursor.execute(sql,values)
                mydb.commit()
            except Exception as e:
                print(e)
            # mycursor.close()
            customerId = {"message": str(projId)}
            return jsonify(customerId)