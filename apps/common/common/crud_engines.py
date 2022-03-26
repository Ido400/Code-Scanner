from manage_mongo import MongoDB
from enum_mongo import Mongo
from documents.engine_documnet import Engine

class CRUDEngines:
   
    def __init__(self, mongo:Mongo) -> None:
        self.mongo = MongoDB(**mongo)
        self.engine_col = "engines"
    
    def create_engine_doc(self, 
                                user_id:str, 
                                folder_name:str, 
                                file_name:str, 
                                description:str,
                                lines:list):
        try:
            engine = Engine(    user_id, 
                                folder_name,
                                file_name, 
                                description,
                                lines)
            self.mongo.insert_to_col(self.engine_col, engine.dict())
        except:
            pass
    
    def update_engine_doc(self, engine:Engine):
        try:
            query = engine.user_id.dict()
            self.mongo.insert_to_col(self.engine_col, engine.dict(), query)
        except:
            pass
    
    def delete_engine_doc(self, engine:Engine):
        try:
            query = engine.user_id.dict()
            self.mongo.delete_document(self.engine_col, query)
        except:
            pass
    
    def get_engines_docs(self):
        try:
            data = self.mongo.get_col(self.engine_col)
            engines = [Engine(**engine) for engine  in list(data)]
            return engines
        except:
            pass

