import json
import os
import urllib3

def slackNotify(data: dict):
    payload = {
        "text": "\n".join(
            f"*{key}*: {value}"
            for key, value in data.items()
            if value not in (None, "", "None")
        )
    }
    encoded_data = json.dumps(payload).encode("utf-8")
    endpoint = os.environ["slack_channel"]
    http = urllib3.PoolManager()
    http.request("POST", endpoint, body=encoded_data)