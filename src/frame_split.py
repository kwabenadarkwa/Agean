import os
import pathlib
from typing import Tuple

import ffmpeg
from event_pipeline.base import EventBase

from DownloadVideo import DownloaderReturnType

vidoes_path = "Videos"


class FrameSplitReturnType:
    """This class represents the return type of the `split_video_into_frames` function."""

    def __init__(self, DownloaderReturnType, frames_path):
        self.DownloaderReturnType = DownloaderReturnType
        self.frames_path = frames_path

    def __str__(self):
        return f"Title: {self.DownloaderReturnType.title
        }\nVideo Link: {self.DownloaderReturnType.link
        }\nTranscript: {self.DownloaderReturnType.transcript
        }\nFrames Path: {self.frames_path}"


class SplitVideoIntoFrames(EventBase):
    def process(
        self, frame_extraction_fps, *args, **kwargs
    ) -> Tuple[bool, FrameSplitReturnType]:
        """This function splits a video into frames.
        Args:
            video (youtube_downloader.DownloaderReturnType): The video to split into frames.
            fps (int): The frames per second to split the video into.
        Returns:
            FrameSplitReturnType: The return type of the function.
        Raises:
        """

        previous_result: DownloaderReturnType = self.previous_result[0].content
        create_folder_with_video_name(previous_result)

        ffmpeg.input(previous_result.filepath).filter(
            "fps", fps=frame_extraction_fps
        ).output(
            filename=pathlib.Path(vidoes_path, previous_result.title, "frame%d.jpg"),
            start_number=1,
        ).overwrite_output().run()

        remove_video(previous_result)
        return True, FrameSplitReturnType(
            previous_result, pathlib.Path(vidoes_path, previous_result.title)
        )


def create_folder_with_video_name(
    video: DownloaderReturnType,
) -> None:
    os.mkdir(pathlib.Path(vidoes_path, video.title))


def remove_video(video: DownloaderReturnType) -> None:
    os.remove(video.filepath)
