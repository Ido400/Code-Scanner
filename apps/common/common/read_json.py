from common.read_data_strategy import ReadData

class ReadJson(ReadData):
    def read_data(self, data: str) ->dict:
        import json
        return json.loads(data)