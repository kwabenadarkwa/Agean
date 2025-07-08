from event_pipeline.fields import InputDataField
from event_pipeline.pipeline import BatchPipeline, Pipeline

from download_video import DownloadVideo
from extract_code import ExtractCodeFromFrames
from frame_split import SplitVideoIntoFrames
from remove_duplicates import RemoveDuplicates

# TODO: the only reason this is here is so that it will be using in the pointy language




class CodeExtractionPipeline(Pipeline):
    # INFO: I think this defines that the pipeline will take a youtube url
    # as input and have 10 of those
    youtube_object = InputDataField(data_type=str, required=True, batch_size=1)
    frame_extraction_fps = InputDataField(data_type=int, required=True)
    duplicate_removal_threshold = InputDataField(data_type=float, required=True)


class BatchExtractionPipeline(BatchPipeline):
    pipeline_template = CodeExtractionPipeline
    listen_to_signals = ["task_completed", "task_failed"]
