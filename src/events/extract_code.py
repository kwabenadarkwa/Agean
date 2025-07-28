import pathlib
from typing import Dict, Tuple

import pytesseract
from event_pipeline.base import EventBase
from PIL import Image

from models import frame_split_type
import utils
import json


#TODO: use the google vision api to extract the text from the frames
class ExtractCodeFromFrames(EventBase):
    def process(self, *args, **kwargs) -> Tuple[bool, Dict[str, str]]:
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
        utils.remove_file(video)
        return True, frame_num_and_content


# INFO: this is the naive solution assuming that the tutorial isn't being scrolled through
def extract_content(video, frame_name):
    # FIX: passing the video object around like this is bad
    return pytesseract.image_to_string(
        Image.open(str(pathlib.Path(video.frames_path, frame_name)))
    )
