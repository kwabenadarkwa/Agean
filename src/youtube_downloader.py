from pytubefix import YouTube
# from pytubefix.cli import on_progress


class DownloaderReturnType:
    ## INFO: there is no need to return the output path because the output path is the default one
    def __init__(self, title, link, transcript):
        self.title = title
        self.link = link
        ##TODO: it is possible that I might have to change this to a dictionary or something and need it later
        self.transcript = transcript

    def __str__(self):
        return f"Title: {self.title
        }\nVideo Link: {self.link
        }\nTranscript: {self.transcript}"


class YoutubeDownloader:
    def __init__(self, link: str) -> None:
        self.link = link

    def download_video(self) -> DownloaderReturnType:
        yt = YouTube(self.link)
        ys = yt.streams.get_highest_resolution()
        ys.download(output_path="Videos")
        return DownloaderReturnType(
            yt.title, self.link, yt.captions["en"].generate_srt_captions()
        )
