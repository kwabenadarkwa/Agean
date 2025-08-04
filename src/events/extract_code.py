import json
import pathlib
from typing import Dict, Tuple

import pytesseract
from event_pipeline.base import EventBase
from PIL import Image

import utils
from models import frame_split_type


# TODO: use the google vision api to extract the text from the frames
class ExtractCodeFromFrames(EventBase):
    def process(self) -> Tuple[bool, Dict[str, str]]:
        video: frame_split_type.FrameSplitReturnType = (
            self.previous_result.first().content  # type:ignore
        )
        frame_names = utils.load_frame_names(video)
        # FIX: might be useful to remove the frames that don't contain code
        frame_num_and_content: Dict[str, str] = {}

        for frame_name in frame_names:
            frame_num_and_content[frame_name[len("frame") : -len(".png")]] = (
                extract_content(video, frame_name)
            )
        print(json.dumps(frame_num_and_content))
        utils.remove_thing_based_on_type(video)
        return True, frame_num_and_content


class TestExtractCodeFromFrames(EventBase):
    def process(self) -> Tuple[bool, Dict[str, str]]:
        level = utils.get_test_videos_level()
        video: frame_split_type.FrameSplitReturnType = (
            self.previous_result.first().content  # type:ignore
        )
        frame_names = utils.load_frame_names(video)
        frame_num_and_content: Dict[str, str] = {}

        for frame_name in frame_names:
            frame_num_and_content[frame_name[len("frame") : -len(".png")]] = (
                extract_content(video, frame_name)
            )
        print(json.dumps(frame_num_and_content))
        create_file_with_video_name(
            level, video.DownloaderReturnType.title, frame_num_and_content
        )
        return True, frame_num_and_content


def create_file_with_video_name(
    level: int,
    filename: str,
    content: Dict[str, str],
) -> None:
    import os

    with open(
        pathlib.Path("expectedData", f"Level{str(level)}", f"{filename}.json"), "w"
    ) as f:
        f.write(json.dumps(content, indent=2))


def extract_content(video, frame_name):
    # FIX: passing the video object around like this is bad
    return pytesseract.image_to_string(
        Image.open(str(pathlib.Path(video.frames_path, frame_name)))
    )
