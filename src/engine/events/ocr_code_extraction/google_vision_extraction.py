import json
import os
import pathlib
from typing import Dict, Tuple

from dotenv import load_dotenv
from event_pipeline.base import EventBase
from google.cloud import vision
from google.oauth2 import service_account
from PIL import Image

import utils
from models import frame_split_type

load_dotenv()


class GoogleVisionExtractCodeFromFrames(EventBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        credentials_info = {
            "type": "service_account",
            "project_id": os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
            "private_key_id": os.getenv("GOOGLE_CLOUD_PRIVATE_KEY_ID"),
            "private_key": os.getenv("GOOGLE_CLOUD_PRIVATE_KEY").replace("\\n", "\n"),  # type: ignore
            "client_email": os.getenv("GOOGLE_CLOUD_CLIENT_EMAIL"),
            "client_id": os.getenv("GOOGLE_CLOUD_CLIENT_ID"),
            "auth_uri": os.getenv("GOOGLE_CLOUD_AUTH_URI"),
            "token_uri": os.getenv("GOOGLE_CLOUD_TOKEN_URI"),
        }

        credentials = service_account.Credentials.from_service_account_info(
            credentials_info
        )
        self.client = vision.ImageAnnotatorClient(credentials=credentials)

    def process(self) -> Tuple[bool, Dict[str, str]]:
        video: frame_split_type.FrameSplitReturnType = (
            self.previous_result.first().content  # type:ignore
        )
        frame_names = utils.load_frame_names(video)
        frame_num_and_content: Dict[str, str] = {}

        for frame_name in frame_names:
            frame_num_and_content[frame_name[len("frame") : -len(".png")]] = (
                self.extract_content(video, frame_name)
            )
        print(json.dumps(frame_num_and_content))
        utils.remove_thing_based_on_type(video)
        return True, frame_num_and_content

    @staticmethod
    def create_file_with_video_name(
        level: int,
        filename: str,
        content: Dict[str, str],
    ) -> None:
        with open(
            pathlib.Path("expected_data", f"Level{str(level)}", f"{filename}.json"), "w"
        ) as f:
            f.write(json.dumps(content, indent=2))

    def extract_content(self, video, frame_name):
        image_path = pathlib.Path(video.frames_path, frame_name)

        with open(image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = self.client.text_detection(image=image)
        texts = response.text_annotations

        if texts:
            # TODO: maybe it might be a sensible step to figure out which bounding box contains the code elements.
            # so maybe instead of actually finding the bouding box. we send the texts object that is extracted. we comb through the texts object
            # to find which of the descriptions actually contains code. and then remove the ones that don't. that could be a step after this point
            return texts[0].description

        if response.error.message:
            raise Exception(f"{response.error.message}")

        return ""
