from event_pipeline.fields import InputDataField
from event_pipeline.pipeline import Pipeline

from download_video import DownloadVideo
from extract_code import ExtractCodeFromFrames
from frame_split import SplitVideoIntoFrames
from remove_duplicates import RemoveDuplicates


class CodeExtractionPipeline(Pipeline):
    # INFO: I think this defines that the pipeline will take a youtube url
    # as input and have 10 of those
    youtube_link = InputDataField(data_type=str, required=True)
    frame_extraction_fps = InputDataField(data_type=int, required=True)
    duplicate_removal_threshold = InputDataField(data_type=float, required=True)


# class BatchExtractionPipeline(BatchPipeline):
#     pipeline_template = ExtractionPipeline
#     listen_to_signals = [SoftSignal('task_completed'), SoftSignal('task_failed')]
#



