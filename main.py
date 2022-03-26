import requests
import json
file = "print('hello')"

data = json.dumps({"file":{"dir_name":"ido", "file_name":"ido_.py", "file_data":file}, "user":{"user_name":"dan"}})
requests.post("http://localhost:8000/dir/file", data=data)