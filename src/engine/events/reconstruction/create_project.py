import os
import re
from ...constants import DEFAULT_LEVEL
from pathlib import Path
from typing import Tuple, Union

from dotenv import load_dotenv
from event_pipeline.base import EventBase
from openai import OpenAI

from ...models.prompt_data import (FileCreationPromptData,
                                   FrameExtractionPromptData)
from ...models.test_data import YoutubeObject
from ...utils import (load_prompt_data_for_file_creation,
                      load_prompt_for_frame_parsing)

load_dotenv()
file_creation_prompt_data: FileCreationPromptData = load_prompt_data_for_file_creation()
frame_extraction_prompt_data: FrameExtractionPromptData = (
    load_prompt_for_frame_parsing()
)


class CreateProject(EventBase):
    def process(
        self, youtube_object: list[YoutubeObject]
    ) -> Tuple[bool, Union[str, None]]:

        client = OpenAI(
            api_key=f"{os.getenv("DEEPSEEK_API_KEY")}",
            base_url="https://api.deepseek.com",
        )
        # level_info = self.get_level_data()
        input_data = self.previous_result.first().content  # type:ignore

        youtube_info = f"""
        YouTube Video Information:
        - Title: {youtube_object[0].title}
        - Link: {youtube_object[0].link}
        - Duration: {youtube_object[0].duration}

        Please include this information as a comment header in the generated Python file to attribute the source.
        """

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": f"{file_creation_prompt_data.your_role}"},
                {
                    "role": "user",
                    "content": f"App Description: \n{file_creation_prompt_data.app_description}\
                            \nReconstruction Guidelines: \n{file_creation_prompt_data.reconstruction_guidelines}\
                            \nAttribution Requirements: \n{file_creation_prompt_data.attribution_requirements}\
                            \nOutput Format: \n{file_creation_prompt_data.output_format}\
                            \nYouTube Video Context: \n{youtube_info}\
                            \nFrame Data Input: \n{input_data}\
                    ",
                },
            ],
            temperature=0.4,
            stream=False,
        )

        generated_code = response.choices[0].message.content
        print(generated_code)

        #TODO: remove the file creation point from here and let the pipeline generate the text file for the server side
        file_path = self._save_generated_file(youtube_object, generated_code)

        with open("response.py", "a") as f:
            # f.write(f"\n--- Generated file: {file_path} ---\n")
            f.write(str(generated_code))

        return True, f"Generated Python file: {file_path}"

    def _save_generated_file(
        self, youtube_object: list[YoutubeObject], code_content: str
    ) -> str:
        safe_title = re.sub(r"[^\w\s-]", "", youtube_object[0].title)
        safe_title = re.sub(r"[-\s]+", "_", safe_title).strip("_")

        output_dir = Path("generated_projects")
        output_dir.mkdir(exist_ok=True)

        file_path = output_dir / f"{safe_title}.py"

        counter = 1
        while file_path.exists():
            file_path = output_dir / f"{safe_title}_{counter}.py"
            counter += 1

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code_content)

        return str(file_path)


