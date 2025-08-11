from event_pipeline.fields import InputDataField
from event_pipeline.pipeline import BatchPipeline, Pipeline
from event_pipeline.signal.signals import event_execution_init, pipeline_pre_init, pipeline_post_init 
from event_pipeline.decorators import listener 

from events import (
    DownloadVideo,
    PytesseractExtractCodeFromFrames,
    SplitVideoIntoFrames,
    RemoveDuplicates,
    LLMParse,
    DetectBoundingBox,
    CropFrames,
    RemoveNonCodeFramesRuleBased,
    RemoveNonCodeFramesWithModel,
)
from models.test_data import YoutubeObject 


class CodeExtractionPipeline(Pipeline):
    youtube_object = InputDataField(data_type=list, batch_size=1)
    frame_extraction_fps = InputDataField(data_type=int, required=True)
    duplicate_removal_threshold = InputDataField(data_type=float, required=True)
    level = InputDataField(data_type=int, required=True)


class TestBatchExtractionPipeline(BatchPipeline):
    pipeline_template = CodeExtractionPipeline



@listener([event_execution_init,pipeline_pre_init,pipeline_post_init], sender=CodeExtractionPipeline) 
def simple_listener(**kwargs):
    print(kwargs) 
