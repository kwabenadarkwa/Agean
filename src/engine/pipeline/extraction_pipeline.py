from event_pipeline.fields import InputDataField
from event_pipeline.pipeline import BatchPipeline, Pipeline

from ..events import (CreateProject, CropFrames, DetectBoundingBox,
                      DownloadVideo, GoogleVisionExtractCodeFromFrames,
                      LLMParse, RemoveDuplicates, RemoveNonCodeFramesRuleBased,
                      RemoveNonCodeFramesWithModel, SplitVideoIntoFrames)
from ..models.test_data import YoutubeObject


class CodeExtractionPipeline(Pipeline):
    youtube_object = InputDataField(data_type=list, batch_size=1)
    frame_extraction_fps = InputDataField(data_type=int, required=True)
    duplicate_removal_threshold = InputDataField(data_type=float, required=True)
    level = InputDataField(data_type=int, required=True)


class TestBatchExtractionPipeline(BatchPipeline):
    pipeline_template = CodeExtractionPipeline
