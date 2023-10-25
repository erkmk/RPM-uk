import requests
import json


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


def check_url(url):
    
    try: 
        print("MY URL",url)
        pattern = r'^[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*$'
        if re.match(pattern, url):
            print("UNC Exists")
            return True
        elif requests.get(url).status_code == 200:
            
            print("URL exists!")
            return True

        else: 
            print("URL does not exist!")
            return False
    except requests.RequestException: 
        print("Invalid URL") 
        return False