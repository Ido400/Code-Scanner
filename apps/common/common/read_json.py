import logging

from common.read_data_strategy import ReadData
from common.logging_controller import exception

LOGGER = logging.getLogger(__name__)

@exception(LOGGER)
class ReadJson(ReadData):
    def read_data(self, data: str) ->dict:
        """
        This method will converte the data into json.

        Args:
        -----
            data(str): The data that will be converted.
        """
        import json
        try:
            return json.loads(data)
        except ValueError:
            raise ValueError("Can't convert data into json")
            