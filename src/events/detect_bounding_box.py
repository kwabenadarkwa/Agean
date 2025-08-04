import pathlib
from typing import Dict, Tuple

import bounding_box_detector_pkg as bbox
from event_pipeline.base import EventBase
from PIL import Image

import utils
from models import frame_split_type


class DetectBoundingBox(EventBase):
    def process(
        self,
    ) -> Tuple[bool, bbox.BoundingBoxReturnType]:
        """
        This function detects the bounding box of the video.
        It does this by using the `detectBoundingBox` function from the `bounding_box_detector_pkg` module. 
        The module is adapted from PS2CODE's work. I packaged it in a different way so that I can use it in my pipeline. 
        """

        frameSplitReturn: frame_split_type.FrameSplitReturnType = (
            self.previous_result.first().content  # type:ignore
        )
        result: bbox.BoundingBoxReturnType = bbox.detectBoundingBox(frameSplitReturn)

        return True, result
