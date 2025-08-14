class DownloaderReturnType:
    """This class represents the return type of the `download_video` function."""

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __getstate__(self):
        return self.__dict__

    def __init__(self, title, filepath, transcript):
        self.title = title
        self.filepath = filepath
        self.transcript = transcript

    def __str__(self):
        return f"Title: {self.title
        }\nTranscript: {self.transcript}"
