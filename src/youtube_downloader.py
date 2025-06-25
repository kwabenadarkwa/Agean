import pathlib
from pytubefix import YouTube
# from pytubefix.cli import on_progress


class DownloaderReturnType:
    ## INFO: there is no need to return the output path because the output path is the default one
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
    yt = YouTube(link)
    filepath = pathlib.Path("Videos", yt.title + ".mp4")
    ys = yt.streams.get_highest_resolution()
    ys.download(output_path="Videos")
    return DownloaderReturnType(
        yt.title, link, filepath, yt.captions["en"].generate_srt_captions()
    )
