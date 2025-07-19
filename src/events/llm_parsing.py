import json
import os
from parser.flags_parser import args as level_args
from typing import Dict, Tuple

import requests
from dotenv import load_dotenv
from event_pipeline.base import EventBase

from models.prompt_data import PromptData
from utils import load_prompt_data
from openai import OpenAI

load_dotenv()
prompt_data: PromptData = load_prompt_data()


# TODO: think about giving the AI some examples that it could use to give me a good response
# TODO: add information about the video in question
class LLMParse(EventBase):
    def process(self, *args, **kwargs) -> Tuple[bool, str]:
        # add to the batch pipeline portion of things
        address = f"http://{os.getenv("SERVER_IP")}/api/generate"

        level_info = self.get_level_data()
        input_data = self.previous_result.first().content  # type:ignore

        prompt = {
            "model": "deepseek-r1:7b",
            # "prompt": f"{prompt_data.app_description}\n"
            # f"Your role:\n{prompt_data.your_role}\n"
            # f"Input description:\n{prompt_data.input_description}\n"
            # f"Output description:\n{prompt_data.output_description}\n"
            # f"Level preamble:\n{prompt_data.level_preamble}\n"
            # f"Level info:\n{level_info}\n"
            # f"Input:\n{input_data}",
            "prompt": "you are a boy can you tell me how to program in python",
        }
        response = requests.post(
            url=address,
            headers={"Content-Type": "application/json"},
            data=json.dumps(prompt),
        )

        print(dict(response.json()))
        # write the response to a file
        with open("response.txt", "w") as f:
            f.write(response.text)
        # the reponse might be an issue at this point
        return True, response.text

    def get_level_data(self) -> str:
        match level_args.level:
            case 1:
                return prompt_data.level_1
            case 2:
                return prompt_data.level_2
            case 3:
                return prompt_data.level_3
            case 4:
                return prompt_data.level_4
            case _:
                return prompt_data.level_1


if __name__ == "__main__":
    pass
