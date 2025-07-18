class FrameSplitReturnType:
    """This class represents the return type of the `split_video_into_frames` function."""

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __getstate__(self):
        return self.__dict__

    def __init__(self, DownloaderReturnType, frames_path):
        self.DownloaderReturnType = DownloaderReturnType
        self.frames_path = frames_path

    def __str__(self):
        return f"Title: {self.DownloaderReturnType.title
        }\nVideo Link: {self.DownloaderReturnType.link
        }\nTranscript: {self.DownloaderReturnType.transcript
        }\nFrames Path: {self.frames_path}"


