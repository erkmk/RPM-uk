from controllers.auth import ClientAccess
from common_util import checkLogin
from flask import send_file

class Download(ClientAccess):
    def get(self, loc, name):
        print("inside download endpoint")
        path = loc.replace("\\", "/") + name
        # if(name == "template"):
        #   path = loc.split("-")[1].replace("\\","/")
        # path = "C:\\RapidPM\\RapidPM\\a10-exception-report-v101.docx"
        # try:
        return send_file(path, as_attachment=True)