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
from .ocr_code_extraction import PytesseractExtractCodeFromFrames, GoogleVisionExtractCodeFromFrames 
from .frame_split import SplitVideoIntoFrames
from .reconstruction import LLMParse 
from .remove_duplicates import RemoveDuplicates

from .code_frame_filtering import RemoveNonCodeFramesRuleBased, RemoveNonCodeFramesWithModel

__all__ = [
    "CropFrames",
    "DetectBoundingBox", 
    "DownloadVideo",
    "PytesseractExtractCodeFromFrames",
    "SplitVideoIntoFrames",
    "LLMParse",
    "RemoveDuplicates",
    
    # Code frame filtering events
    "RemoveNonCodeFramesRuleBased",
    "RemoveNonCodeFramesWithModel",
]
