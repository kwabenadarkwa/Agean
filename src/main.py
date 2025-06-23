import youtube_downloader 
if __name__ == "__main__":
    video = youtube_downloader.YoutubeDownloader('http://youtube.com/watch?v=2lAe1cqCOXo')
    video.download_video()

