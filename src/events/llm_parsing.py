import json
import os
from typing import Dict, Tuple

import requests
from dotenv import load_dotenv
from event_pipeline.base import EventBase

load_dotenv()


# TODO: think about giving the AI some examples that it could use to give me a good response
class LLMParse(EventBase):
    def process(self, *args, **kwargs) -> Tuple[bool, Dict[str, str]]:
        address = f"http://{os.getenv("SERVER_IP")}/api/generate"
        prompt = 
        response = requests.post(
            url=address,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"model": "deepseek-r1:7b", "prompt": "Hello, world!"}),
        )
        print(response.text)


if __name__ == "__main__":
    pass
