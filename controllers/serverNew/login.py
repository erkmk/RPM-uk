from controllers.auth import ClientAccess
import json
import jwt
from common_util import checkLogin


class Login(ClientAccess):
    def get(self, userEmail, userPassword):
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
