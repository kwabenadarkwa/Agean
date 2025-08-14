import pathlib
from typing import Dict, Tuple

import bounding_box_detector_pkg as bbox
from event_pipeline.base import EventBase
from PIL import Image

from .. import utils
from ..models import frame_split_type


class DetectBoundingBox(EventBase):
    # TODO: add the VID2XML one and then have a test for that too to show the level of accuracy you
    # get in the output(with respect AI model that they are using)
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
        # TODO:check to see what the accuracy of this is
        result: bbox.BoundingBoxReturnType = bbox.detectBoundingBox(frameSplitReturn)

        return True, result
