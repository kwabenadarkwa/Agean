from event_pipeline.telemetry import (PrometheusPublisher, get_failed_events,
                                      get_metrics, get_retry_stats,
                                      get_slow_events, monitor_events)

from extraction_pipeline import BatchExtractionPipeline, CodeExtractionPipeline
from load_youtube_data import load_youtube_data

if __name__ == "__main__":
    # monitor_events()
    links = []
    data = load_youtube_data("TestData.json")
    links = [youtube_object.link for youtube_object in data.level_1]

    batch = BatchExtractionPipeline(
        youtube_object=links, frame_extraction_fps=1, duplicate_removal_threshold=0.8
    )
    batch.execute()
    #
    # metrics_json = get_metrics()
    # print(metrics_json)

    # failed_events = get_failed_events()
    # slow_events = get_slow_events(threshold_seconds=2.0)
    # retry_stats = get_retry_stats()
