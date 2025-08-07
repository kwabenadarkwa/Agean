import os
import pathlib
from pathlib import Path
from typing import Tuple

import ffmpeg
from event_pipeline.base import EventBase

import constants
import utils
from models import download_type, frame_split_type


class SplitVideoIntoFrames(EventBase):
    def process(
        self, frame_extraction_fps
    ) -> Tuple[bool, frame_split_type.FrameSplitReturnType]:
        """This function splits a video into frames.
        Args:
            video (youtube_downloader.DownloaderReturnType): The video to split into frames.
            fps (int): The frames per second to split the video into.
        Returns:
            FrameSplitReturnType: The return type of the function.
        Raises:
        """

        video_downloaded: download_type.DownloaderReturnType = (
            self.previous_result.first().content  # type:ignore
        )
        create_folder_with_video_name(video_downloaded)

        ffmpeg.input(video_downloaded.filepath).filter(
            "fps", fps=frame_extraction_fps
        ).output(
            filename=pathlib.Path(
                constants.VIDEOS_PATH, video_downloaded.title, "frame%d.jpg"
            ),
            start_number=1,
        ).overwrite_output().run()

        utils.remove_thing_based_on_type(video_downloaded)
        return True, frame_split_type.FrameSplitReturnType(
            video_downloaded,
            pathlib.Path(constants.VIDEOS_PATH, video_downloaded.title),
        )


class DevelopingSplitVideoIntoFrames(EventBase):
    def process(
        self, frame_extraction_fps
    ) -> Tuple[bool, frame_split_type.FrameSplitReturnType]:
        """This function splits a video into frames. This is the development version that is being used to find out which
        method is the best for splitting the video into frames and things that come later in the pipeline.
        Args:
            video (youtube_downloader.DownloaderReturnType): The video to split into frames.
            fps (int): The frames per second to split the video into.
        Returns:
            FrameSplitReturnType: The return type of the function.
        Raises:
        """
        level = utils.get_test_videos_level()

        video_downloaded: download_type.DownloaderReturnType = (
            self.previous_result.first().content  # type:ignore
        )
        create_folder_with_video_name_and_level(level, video_downloaded)

        ffmpeg.input(video_downloaded.filepath).filter(
            "fps", fps=frame_extraction_fps
        ).output(
            filename=pathlib.Path(
                constants.TESTING_VIDEOS_PATH,
                f"Level{str(level)}",
                video_downloaded.title,
                "frame%d.jpg",
            ),
            start_number=1,
        ).overwrite_output().run()

        utils.remove_thing_based_on_type(video_downloaded)
        return True, frame_split_type.FrameSplitReturnType(
            video_downloaded,
            pathlib.Path(constants.TESTING_VIDEOS_PATH, video_downloaded.title),
        )


def create_folder_with_video_name(
    video: download_type.DownloaderReturnType,
) -> None:
    file_path = Path(constants.VIDEOS_PATH, video.title)
    if file_path.exists():
        utils.remove_after_failure(file_path)
    os.mkdir(file_path)


def create_folder_with_video_name_and_level(
    level: int,
    video: download_type.DownloaderReturnType,
) -> None:
    os.mkdir(
        pathlib.Path(constants.TESTING_VIDEOS_PATH, f"Level{str(level)}", video.title)
    )
