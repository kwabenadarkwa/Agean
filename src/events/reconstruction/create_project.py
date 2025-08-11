# think about passing the level during testing.
# pass the name of the json file that's created to the llm
# give it a prompt on all the information is needs to know.
# youtube channel data, name of videos
# this should be the final stagbe

import json
import os
from parser.flags_parser import args as level_args
from typing import Dict, Tuple, Union

from dotenv import load_dotenv
from event_pipeline.base import EventBase
from openai import OpenAI

from models.prompt_data import PromptData
from utils import load_prompt_data

load_dotenv()
prompt_data: PromptData = load_prompt_data()


class CreateProject(EventBase): 
    def process(self) -> Tuple[bool, Union[str, None]]:

        client = OpenAI(
            api_key=f"{os.getenv("DEEPSEEK_API_KEY")}",
            base_url="https://api.deepseek.com",
        )
        level_info = self.get_level_data()
        input_data = self.previous_result.first().content  # type:ignore

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": f"{prompt_data.your_role}"},
                {
                    "role": "user",
                    "content": f"App Description: \n{prompt_data.app_description}\
                            \nInput Description: \n{prompt_data.input_description}\
                            \nOutput Description: \n{prompt_data.output_description}\
                            \nLevel Preamble: \n{prompt_data.level_preamble}\
                            \nLevel Info: \n{level_info}\
                            \nInput: \n{input_data}\
                    ",
                },
            ],
            temperature=0.4,
            stream=False,
        )

        print(response.choices[0].message.content)

        with open("response.txt", "a") as f:
            f.write(str(response.choices[0].message.content))

        return True, response.choices[0].message.content

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
