from pytubefix import YouTube
from pytubefix.cli import on_progress
# class DownloaderReturnTyppe:
#     def __init__(self,video_link,file_location,title,channel_name,video_transcript) -> None:
#         self.video_link = video_link
#         self.file_location = file_location
#         self.title = title
#         self.channel_name = channel_name
#         self.video_transcript = video_transcript
#


class YoutubeDownloader:
    def __init__(self, link: str) -> None:
        self.link = link

    # create function for downloading videos that returns the link to the videos
    # location in the file tree and then data about the video.
    # data: title, youtube channel, video transcript.
    def download_video(self):
        yt = YouTube(self.link, on_progress_callback=on_progress)
        print(yt.title)
        ys = yt.streams.get_highest_resolution()
        ys.download(output_path="Videos")

            

      
