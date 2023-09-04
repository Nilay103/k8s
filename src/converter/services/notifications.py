import json

import requests
from typing import Dict


def send_email_ns(payload_data: Dict):
    requests.post(
        # f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login", auth=basicAuth TODO
        "http://localhost:5055/send_ns", data=json.dumps(payload_data)
    )
    return
