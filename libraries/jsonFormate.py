# JsonFormate.py
from pydantic import BaseModel, Field
import json

class JsonFormate(BaseModel):
    data: dict = Field(default_factory=dict, description="A dictionary containing data.")

    @staticmethod
    def getEncodeData(data):
        # Assuming data is a Row or similar object, convert it to a dictionary
        if hasattr(data, "_asdict"):
            data = data._asdict()
        return JsonFormate(data=data).json()

    @staticmethod
    def getDecodedData(data):
        return json.loads(data)

    @staticmethod
    def getBasicEncoded(data):
        return json.dumps(data)

    @staticmethod
    def getAdvanceEncoded(data):
        d_data = {
            "type": "dict_type",
            "data": [data],
            "input_type": "list"
        }

        return d_data

    @staticmethod
    def getObjectToJson(lst):
        # Convert the list to a JSON string
        json_string = json.dumps(lst)
        return json_string
