import pathlib
from typing import Tuple

from event_pipeline.base import EventBase
from llist import sllist as linkedlist

import utils
from models import frame_split_type

from .config import CodeDetectionConfig
from .detectors import is_code_frame


class RemoveNonCodeFramesRuleBased(EventBase):
    def process(self) -> Tuple[bool, frame_split_type.FrameSplitReturnType]:

        video_frames_info_obj: frame_split_type.FrameSplitReturnType = (
            self.previous_result.first().content  # type:ignore
        )

        frames: linkedlist = utils.load_frame_names(video_frames_info_obj)

        current_frame = frames.first
        assert current_frame is not None, "Failed to load frame names"

        while current_frame is not None:
            frame_path = pathlib.Path(
                video_frames_info_obj.frames_path, current_frame.value
            )

            if not is_code_frame(frame_path, CodeDetectionConfig):
                utils.remove_thing_based_on_type(str(frame_path))

            current_frame = current_frame.next

        return True, video_frames_info_obj
