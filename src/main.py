from event_pipeline.telemetry import (PrometheusPublisher, get_failed_events,
                                      get_metrics, get_retry_stats,
                                      get_slow_events, monitor_events)

from pipeline.extraction_pipeline import BatchExtractionPipeline
from utils import get_youtube_objects_based_on_level,get_test_videos_level

if __name__ == "__main__":
    # monitor_events()
    batch = BatchExtractionPipeline(
        youtube_object=get_youtube_objects_based_on_level(),
        frame_extraction_fps=1,
        duplicate_removal_threshold=0.8,
        level=get_test_videos_level()
    )
    batch.execute()
    #
    # metrics_json = get_metrics()
    # print(metrics_json)

    # failed_events = get_failed_events()
    # slow_events = get_slow_events(threshold_seconds=2.0)
    # retry_stats = get_retry_stats()
