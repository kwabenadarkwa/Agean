import pathlib

from pytubefix import YouTube

# from pytubefix.cli import on_progress


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


def download_video(link) -> DownloaderReturnType:
    """This function downloads a video from a link.
    Args:
        link (str): The link to the video.
    Returns:
        DownloaderReturnType: The return type of the function.
    Raises:
    """
    yt = YouTube(link)
    filepath = pathlib.Path("Videos", yt.title + ".mp4")

    if yt.captions.get("en"):
        captions = yt.captions["en"].generate_srt_captions()
    elif yt.captions.get("a.en"):
        captions = yt.captions["a.en"].generate_srt_captions()
    else:
        captions = None

    ys = yt.streams.get_highest_resolution()
    ys.download(output_path="Videos")
    return DownloaderReturnType(yt.title, link, filepath, captions)
