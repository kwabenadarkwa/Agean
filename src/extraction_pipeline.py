from event_pipeline.fields import InputDataField
from event_pipeline.pipeline import Pipeline


class CodeExtractionPipeline(Pipeline):
    # INFO: I think this defines that the pipeline will take a youtube url as input and have 10 of those
    youtube_link = InputDataField(data_type=str, required=True)
    frame_extraction_fps = InputDataField(data_type=int, required=True)


# class BatchExtractionPipeline(BatchPipeline):
#     pipeline_template = ExtractionPipeline
#     listen_to_signals = [SoftSignal('task_completed'), SoftSignal('task_failed')]
#


if __name__ == "__main__":
    pipeline = CodeExtractionPipeline(
        youtube_link="https://youtu.be/eMR-YWq21b0?si=ICWOIGTARaG8hL3q",
        frame_extraction_fps=1,
        duplicate_removal_threshold=0.8,
    )
    pipeline.start()
