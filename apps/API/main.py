from crypt import methods
from flask import Flask, request

from common.manage_engines import ManageEngines
from common.manage_folder import ManageFolder

URL = ""
app = Flask(__name__)

manage_folder = ManageFolder(URL)
manage_engines = ManageEngines("", "","")
#manage_engines.load_engines(PATH)

@app.route("/user", methods=["POST"])
def create_user():
    pass
@app.route("/user", methods=["GET"])
def get_user():
    pass

@app.route("/dir", methods=["POST"])
def post_dir():
    """
    Post:
        {"dir_name" : ""} 
    """
    data = request.get_json()
    manage_folder.create_dir(data["dir_name"])
   
@app.route("/file", methods=["POST"])
def post_file():
    """
    Post:
        {"user_id":"","dir_name":"","file_name": "", "file":"bytes"}
    """
    data = request.get_json()
    manage_folder.create_file(data["dir_name"], data["file_name"], data["file"])
    manage_engines.load_engines({data['dir_name']}, manage_folder)
    manage_engines.engines_notify(data["user_id"],data['dir_name'],data['file_name'])

@app.route("/file", methods=["PATCH"])
def update_file():
    """
    PATCH:
        {"user_id":"","dir_name":"","file_name": "", "file":"bytes"}
    """
    data = request.get_json()
    manage_folder.create_file(data["dir_name"], data["file_name"], data["file"])
    manage_engines.load_engines({data['dir_name']}, manage_folder)
    manage_engines.engines_notify(data["user_id"],data['dir_name'],data['file_name'])

@app.route("/plugins", methods=["POST"])
def post_plugins():
    """
    {"data":{"plugins":[], "engines":[]}, "dir_name":""}
    """
    data = request.get_json()
    manage_folder.create_file(data["dir_name"], "plugins.json", data["data"])

app.run(host="localhost", port=5000,debug=True)