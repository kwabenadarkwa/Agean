import youtube_downloader 
if __name__ == "__main__":
    video = youtube_downloader.YoutubeDownloader('http://youtube.com/watch?v=2lAe1cqCOXo')
    youtube_vid = video.download_video()
    print(youtube_vid)

