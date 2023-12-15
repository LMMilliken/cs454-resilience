from typing import Dict
import requests

targets: Dict[str, str] = {}


def notify(message: str, channel: str = "logs"):
    if channel not in targets:
        return "channel not found in targets"
    url = targets[channel]
    headers = {"Content-type": "application/json"}
    data = '{"text": "' + message + '"}'

    response = requests.post(url, headers=headers, data=data)
    return str(response)
