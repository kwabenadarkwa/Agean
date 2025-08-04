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
    ):

        frameSplitReturn: frame_split_type.FrameSplitReturnType = (
            self.previous_result.first().content# type:ignore
        )  
        result = bbox.detectBoundingBox(frameSplitReturn)

        return True,  result
