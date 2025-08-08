from typing import Tuple
from event_pipeline.base import EventBase
from llist import sllist as linkedlist

import constants
import utils
from models import frame_split_type

class RemoveNonCodeFramesRuleBased(EventBase): 
    def process(self) -> Tuple[bool, frame_split_type.FrameSplitReturnType]:
        video_frames_info_obj: frame_split_type.FrameSplitReturnType = (
            self.previous_result.first().content  # type:ignore
        )
        """
        """
        frames = utils.load_frame_names(video_frames_info_obj) 


        return True, video_frames_info_obj

    @staticmethod
    def load_images_as_np_array(
        video_frames_info_obj: frame_split_type.FrameSplitReturnType,
    ) -> None:
        pass
   
    @staticmethod
    def remove_non_code_frames_based_on_classification():
        pass       