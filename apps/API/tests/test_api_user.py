import sys
import os
import motor
from beanie import init_beanie
from fastapi.testclient import TestClient
from common.documents.user_document import User
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

MONGO_CONNECTION_STRING = "mongodb://root:Aa123456@localhost:27017/"


def test_1_insert_user():
    with TestClient(app) as client:
        data = {"user_name":"deafult_test"}
        response = client.post("/user", json=data)
        assert response.status_code, 200

def test_2_get_user():
    with TestClient(app) as client:
        response = client.get(f"/user/deafult_test")
        assert response.status_code, 200

def test_3_update_user():
    with TestClient(app) as client:
        data = {"user_name":"deafult_test_update", "dir_name": ["ido"]}
        response = client.put("/user", json=data)
        assert response.status_code, 200

def test_4_upsert_user():
    with TestClient(app) as client:
        data = {"user_name":"deafult_test_upsert", "dir_name": ["ido"]}
        response = client.put("/user/upsert", json=data)
        assert response.status_code, 200

def test_5_insert_400():
    with TestClient(app) as client:
        data = {"user_name":"deafult_test_upsert", "dir_name": ["ido"]}
        response = client.post("/user", json=data) 
        assert response.status_code, 400

def test_6_get_400():
    with TestClient(app) as client:
        response = client.get("/user/-1")
        assert response.status_code, 400

def test_7_update_404():
    with TestClient(app) as client:
        data = {"user_name":"-1", "dir_name": ["ido"]}
        response = client.put("/user", json=data)
        assert response.status_code, 200

def test_8_delete_user():
    with TestClient(app) as client:
        response = client.delete("/user/deafult_test")
        assert response.status_code, 200
        response = client.delete("/user/deafult_test_upsert")
        assert response.status_code, 200

