from apps.common.common.manage_mongo import MongoDB
from documents.user_document import User

class CRUDUsers:
    def __init__(self, mongo:MongoDB) -> None:
        self.mongo = mongo
        self.user_col = "users"
  
    def create_user(self, user_name:str, folders:list, engines:dict) ->User:
        try:
            user = User(user_name, folders, engines)
            id_ = self.mongo.insert_document_get_id(self.user_col, user.dict())
            user.user_id = str(id_)
            return user
        except:
            pass

    def get_user(self, user:User):
        try:
            data = self.mongo.get_col_query(self.user_col, user.user_id.dict())
            user = list(data)[0]
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
    
  