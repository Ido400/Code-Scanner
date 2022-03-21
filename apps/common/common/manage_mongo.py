import pymongo
from bson.objectid import ObjectId

class MongoDB:
    def __init__(self, host:str,password:str, user:str, port:str, db:str):
        try:
            self.client = pymongo.MongoClient(f"mongodb://{user}:{password}@{host}:{port}/")
            self.client.server_info()
            self.db = self.client[db]
        except Exception:
            pass

    def insert_to_col(self, col:str, data:dict, query:dict={}):
        try:
            mycol = self.db[col]
            mycol.update(query, data, upsert=True)
        except Exception:
            pass

    def get_col(self,col) ->iter:
        try:
            mycol = self.db[col]
            for item in mycol.find():
                yield item
        except Exception:
            pass
        
    def get_col_query(self,col:str, query:dict, value_define:dict={})->iter:
        try:
            mycol = self.db[col]
            for item in mycol.find(query, value_define):
                yield item
        except Exception:
            pass
    def delete_document(self, col:str, query:dict):
        try:
            mycol = self.db[col]
            mycol.delete_one(query)
        except Exception:
            pass
    def insert_document_get_id(self, col:str, data:dict) -> ObjectId:
        try:
            data["_id"] = ObjectId()
            mycol = self.db[col]
            mycol.insert(data)
            return data["_id"]
        except Exception:
            pass
    # def insert_many(self, col:str , data:dict, query={}):
    #     mycol = self.db[col]
    #     mycol.update_many()