import json

import requests
from typing import Dict

from configs import NOTIFICATION_SVC_ADDRESS


def send_email_ns(payload_data: Dict):
    requests.post(
        f"http://{NOTIFICATION_SVC_ADDRESS}/send_ns", data=json.dumps(payload_data)
    )
    return
