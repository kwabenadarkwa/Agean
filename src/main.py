import youtube_downloader
import frame_split
import remove_duplicates
import extract_code

if __name__ == "__main__":
    youtube_vid = youtube_downloader.download_video(
        "https://youtu.be/eMR-YWq21b0?si=ICWOIGTARaG8hL3q"
    )
    print(youtube_vid)
    print("after downloading")
    frames = frame_split.split_video_into_frames(youtube_vid, fps=1)
    #no optimization version of the application
    # remove_duplicates.remove_duplicates(frames, threshold=0.2)
    print(extract_code.extract_code_from_video(frames))
