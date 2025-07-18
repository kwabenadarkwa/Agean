from event_pipeline.fields import InputDataField
from event_pipeline.pipeline import BatchPipeline, Pipeline

from download_video import DownloadVideo
from extract_code import ExtractCodeFromFrames
from frame_split import SplitVideoIntoFrames
from load_youtube_data import YoutubeObject
from remove_duplicates import RemoveDuplicates



class CodeExtractionPipeline(Pipeline):
    # TODO: currently this is a string but it should be a YoutubeObject
    youtube_object = InputDataField(data_type=list, batch_size=1)
    frame_extraction_fps = InputDataField(data_type=int, required=True)
    duplicate_removal_threshold = InputDataField(data_type=float, required=True)


class BatchExtractionPipeline(BatchPipeline):
    pipeline_template = CodeExtractionPipeline
    listen_to_signals = ["task_completed", "task_failed"]
