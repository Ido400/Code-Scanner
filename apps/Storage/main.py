from flask import Flask, request

from common.errors.dir_exsits import DirNotExists
from common.errors.dir_not_found import DirNotFound

from tools.file_system import FileSystem

app = Flask(__name__)

file_system = FileSystem("./storage_files")

@app.route("/dir",methods=["POST"])
def create_dir() ->str:
    """    
    {"dir_name":""}
    """
    try:
        data = request.get_json()
        file_system.create_dir(data["dir_name"])
        return "OK", 200
    except DirNotExists:
        return "The dir exists", 400
@app.route("/file", methods=["POST"])
def create_file() ->str:
    """
    {"dir_name":"", "file_name":"", "file_data":""}
    """
    try:
        data = request.get_json()
        file_system.create_file(data["dir_name"], data["file_name"], data["file_data"])
        return "OK", 200
    except DirNotFound:
        return "The dir not found", 404

@app.route("/file", methods=["GET"])
def get_file() ->dict:
    """
    {"dir_name":"", "file_name":""}
    """
    try:
        data = request.get_json()
        file = file_system.read_data(data["dir_name"], data["file_name"])
        data["file_data"] = file
        return file
    except FileNotFoundError:
        return "The file not found", 404

if __name__ == "__main__":
    app.run(host="localhost", port=6000, debug=False)