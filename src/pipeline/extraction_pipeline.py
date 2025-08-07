from event_pipeline.fields import InputDataField
from event_pipeline.pipeline import BatchPipeline, Pipeline

from events.download_video import DownloadVideo
from events.extract_code import ExtractCodeFromFrames
from events.frame_split import SplitVideoIntoFrames
from events.remove_duplicates import RemoveDuplicates
from events.llm_parsing import LLMParse
from models.test_data import YoutubeObject
from events.dummy_event import DummyEvent
from events.dummy_event_two import DummyEventTwo
from events.frame_split import DevelopingSplitVideoIntoFrames
from events.detect_bounding_box import DetectBoundingBox 
from events.crop_frames import CropFrames 
from events.remove_non_code_frames import RemoveNonCodeFrames 


class CodeExtractionPipeline(Pipeline):
    youtube_object = InputDataField(data_type=list, batch_size=1)
    frame_extraction_fps = InputDataField(data_type=int, required=True)
    duplicate_removal_threshold = InputDataField(data_type=float, required=True)
    level = InputDataField(data_type=int, required=True)


class TestBatchExtractionPipeline(BatchPipeline):
    pipeline_template = CodeExtractionPipeline
