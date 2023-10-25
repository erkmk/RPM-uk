from flask import request
from controllers.auth import ClientAccess


class Upload(ClientAccess):
    def post(self,):
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