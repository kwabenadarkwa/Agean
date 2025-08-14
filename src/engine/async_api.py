import asyncio
from concurrent.futures import ThreadPoolExecutor

from models.test_data import YoutubeObject
from pipeline.extraction_pipeline import CodeExtractionPipeline


async def extract_code_async(
    youtube_object: list[YoutubeObject],
    frame_extraction_fps: int,
    duplicate_removal_threshold: float,
    level: int,
):
    """
    Async wrapper for code extraction pipeline.
    Runs pipeline in thread pool to avoid blocking event loop to allow for processing of multiple requests at the same time.
    """
    loop = asyncio.get_event_loop()

    def run_pipeline():
        pipeline = CodeExtractionPipeline(
            youtube_object=youtube_object,
            frame_extraction_fps=frame_extraction_fps,
            duplicate_removal_threshold=duplicate_removal_threshold,
            level=level,
        )
        return pipeline.start()

    # Run in thread pool executor
    with ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, run_pipeline)

    # INFO: this returns an execution context object which isn't what we want in particular so remember to change what happens in the end
    return result
