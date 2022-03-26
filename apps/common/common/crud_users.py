from manage_mongo import MongoDB
from enum_mongo import Mongo
from documents.user_document import User

class CRUDUsers:
    def __init__(self, mongo:Mongo) -> None:
        self.mongo = MongoDB(**mongo)
        self.user_col = "users"
  
    def create_user(self, user_name:str) ->User:
        try:
            user = User(user_name, [], {})
            id_ = self.mongo.insert_document_get_id(self.user_col, user.dict())
            user.user_id = str(id_)
            return user
        except:
            pass

    def get_user(self, user_id:dict):
        try:
            data = list(self.mongo.get_col_query(self.user_col, user_id))[0]
            user = User(**data)
            return user
        except:
            pass

    def get_users(self):
        try:
            data = self.mongo.get_col_query(self.user_col, {})
            users = [User(**user) for user in list(data)]
            return users
        except:
            pass
        
    def update_user(self, user:User):
        try:
            query = user.user_id.dict()
            self.mongo.insert_to_col(self.user_col,user.dict(), query)
        except Exception:
            pass
    
  