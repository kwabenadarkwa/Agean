"""
Events package containing all pipeline event processors.

This package provides modular event processors that can be used in video
processing pipelines. Each event handles a specific step in the pipeline.
"""

from .crop_frames import CropFrames
from .detect_bounding_box import DetectBoundingBox
from .download_video import DownloadVideo
from .dummy_event import DummyEvent
from .dummy_event_two import DummyEventTwo
from .extract_code import ExtractCodeFromFrames
from .frame_split import SplitVideoIntoFrames
from .llm_parsing import LLMParse
from .remove_duplicates import RemoveDuplicates

from .code_frame_filtering import RemoveNonCodeFramesRuleBased, RemoveNonCodeFramesWithModel

__all__ = [
    "CropFrames",
    "DetectBoundingBox", 
    "DownloadVideo",
    "ExtractCodeFromFrames",
    "SplitVideoIntoFrames",
    "LLMParse",
    "RemoveDuplicates",
    
    # Code frame filtering events
    "RemoveNonCodeFramesRuleBased",
    "RemoveNonCodeFramesWithModel",
]
