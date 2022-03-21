from flask import Flask, jsonify, request

from tools.file_system import FileSystem

app = Flask(__name__)

file_system = FileSystem("../storage")

@app.route("/dir",methods=["POST"])
def create_dir():
    """
    {"dir_name":""}
    """
    data = request.get_json()
    file_system.create_dir(data["dir_name"])
    

@app.route("/file", methods=["POST"])
def create_file():
    """
    {"dir_name":"", "file_name":"", "file_data":""}
    """
    data = request.get_json()
    file_system.create_file(data["dir_name"], data["file_name"], data["file_data"])

@app.route("/file", methods=["GET"])
def get_file():
    """
    {"dir_name":"", "file_name":""}
    """
    data = request.get_json()
    file = file_system.read_data(data["dir_name"], data["file_name"])
    data["file_data"] = file
    return jsonify(data)