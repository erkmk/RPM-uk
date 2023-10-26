from controllers.auth import ClientAccess
from flask import request
from flask_jsonpify import jsonify


class GetMyData(ClientAccess):
    def get(self,company_id):
        
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
        
