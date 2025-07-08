import pathlib
from typing import Tuple

from event_pipeline.base import EventBase
from pytubefix import YouTube


class DownloaderReturnType:
    """This class represents the return type of the `download_video` function."""

    def __init__(self, title, link, filepath, transcript):
        self.title = title
        self.link = link
        self.filepath = filepath
        self.transcript = transcript

    def __str__(self):
        return f"Title: {self.title
        }\nVideo Link: {self.link
        }\nTranscript: {self.transcript}"


class DownloadVideo(EventBase):
    def process(
        self, youtube_link, *args, **kwargs
    ) -> Tuple[bool, DownloaderReturnType]:
        """This function downloads a video from a link.
        Args:
            link (str): The link to the video.
        Returns:
            DownloaderReturnType: The return type of the function.
        Raises:
        """
        yt = YouTube(youtube_link)
        filepath = pathlib.Path("Videos", yt.title + ".mp4")

        if yt.captions.get("en"):
            captions = yt.captions["en"].generate_srt_captions()
        elif yt.captions.get("a.en"):
            captions = yt.captions["a.en"].generate_srt_captions()
        else:
            captions = None

        ys = yt.streams.get_highest_resolution()
        ys.download(output_path="Videos")  # type: ignore
        return True, DownloaderReturnType(yt.title, youtube_link, filepath, captions)
