from event_pipeline.telemetry import (get_failed_events, get_metrics,
                                      get_retry_stats, get_slow_events,
                                      monitor_events)

from extraction_pipeline import CodeExtractionPipeline,BatchExtractionPipeline

if __name__ == "__main__":
    monitor_events()
    pipeline = CodeExtractionPipeline(
        youtube_link="https://youtu.be/eMR-YWq21b0?si=ICWOIGTARaG8hL3q",
        frame_extraction_fps=1,
        duplicate_removal_threshold=0.8,
    )
    # pipeline.start()
    simple_batch = BatchExtractionPipeline()
    simple_batch.execute(name)
    metrics_json = get_metrics()
    print(metrics_json)

    failed_events = get_failed_events()
    slow_events = get_slow_events(threshold_seconds=2.0)
    retry_stats = get_retry_stats()
