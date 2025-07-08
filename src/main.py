from extraction_pipeline import CodeExtractionPipeline

if __name__ == "__main__":
    pipeline = CodeExtractionPipeline(
        youtube_link="https://youtu.be/eMR-YWq21b0?si=ICWOIGTARaG8hL3q",
        frame_extraction_fps=1,
        duplicate_removal_threshold=0.8,
    )
    pipeline.start()
