import youtube_downloader
import frame_split

if __name__ == "__main__":
    youtube_vid = youtube_downloader.download_video(
        "http://youtube.com/watch?v=2lAe1cqCOXo"
    )
    print(youtube_vid)
    print("after downloading")
    frame_split.split_video_into_frames(youtube_vid, fps=30)
