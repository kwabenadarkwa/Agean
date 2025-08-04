import pathlib
from typing import Tuple

import cv2 as cv
from event_pipeline.base import EventBase

import utils
from models import frame_split_type


class RemoveNonCodeFrames(EventBase): 
    def process(self) -> Tuple[bool, frame_split_type.FrameSplitReturnType]: 

