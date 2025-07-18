import pathlib
from typing import Tuple

from event_pipeline.base import EventBase
from pytubefix import YouTube

from models import download_type
from models.test_data import YoutubeObject


class DownloadVideo(EventBase):
    def process(
        self, youtube_object:list[YoutubeObject], *args, **kwargs
    ) -> Tuple[bool, download_type.DownloaderReturnType]:
        """This function downloads a video from a link.
        Args:
            link (str): The link to the video.
        Returns:
            DownloaderReturnType: The return type of the function.
        Raises:
        """
        self.stop_on_error = True
        # INFO: the paraamter that is passed inside of the batch pipeline is a list of strings
        # hence to access it we need to access the first element of the list

        yt = YouTube(youtube_object[0].link) 
        filepath = pathlib.Path("Videos", yt.title + ".mp4")

        if yt.captions.get("en"):
            captions = yt.captions["en"].generate_srt_captions()
        elif yt.captions.get("a.en"):
            captions = yt.captions["a.en"].generate_srt_captions()
        else:
            captions = None

        ys = yt.streams.get_highest_resolution()
        ys.download(output_path="Videos")  # type: ignore

        if yt is None:
            # TODO: find something better to return here
            return False, download_type.DownloaderReturnType(None, None, None)

        return True, download_type.DownloaderReturnType(
            yt.title, filepath, captions
        )
