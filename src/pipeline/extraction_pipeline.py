from event_pipeline.fields import InputDataField
from event_pipeline.pipeline import BatchPipeline, Pipeline

from events.download_video import DownloadVideo
from events.extract_code import ExtractCodeFromFrames
from events.frame_split import SplitVideoIntoFrames
from events.remove_duplicates import RemoveDuplicates
from models.test_data import YoutubeObject


class CodeExtractionPipeline(Pipeline):
    youtube_object = InputDataField(data_type=list, batch_size=1)
    frame_extraction_fps = InputDataField(data_type=int, required=True)
    duplicate_removal_threshold = InputDataField(data_type=float, required=True)


class BatchExtractionPipeline(BatchPipeline):
    pipeline_template = CodeExtractionPipeline
    listen_to_signals = ["task_completed", "task_failed"]
