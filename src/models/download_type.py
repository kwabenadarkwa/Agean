class DownloaderReturnType:
    """This class represents the return type of the `download_video` function."""

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __getstate__(self):
        return self.__dict__

    def __init__(self, title, link, filepath, transcript):
        self.title = title
        self.link = link
        self.filepath = filepath
        self.transcript = transcript

    def __str__(self):
        return f"Title: {self.title
        }\nVideo Link: {self.link
        }\nTranscript: {self.transcript}"


