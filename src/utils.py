import json
import os
from os import walk
from typing import Union

from llist import sllist as linkedlist
from natsort import natsorted

from models import download_type, frame_split_type, test_data


def load_youtube_data(file_name: str) -> test_data.TestData:
    with open(file_name, "r") as f:
        data = json.load(f)
        return test_data.TestData(**data)


def load_frame_names(video_frames: frame_split_type.FrameSplitReturnType) -> linkedlist:
    """This function loads the frame names from the video frames.
    Args:
        video_frames (frame_split.FrameSplitReturnType): The video frames to load the frame
        names from.

    Returns:
        linkedlist: The linked list of frame names.

    Raises:
    """

    frame_names = []
    for _, _, filenames in walk(video_frames.frames_path):
        frame_names.extend(filenames)
        break
    frame_names = natsorted(frame_names)
    return linkedlist(frame_names)


def remove_file(
    video: Union[
        download_type.DownloaderReturnType, frame_split_type.FrameSplitReturnType
    ],
) -> None:
    if isinstance(video, download_type.DownloaderReturnType):
        os.remove(video.filepath)
    elif isinstance(video, frame_split_type.FrameSplitReturnType):
        os.remove(video.DownloaderReturnType.filepath)


if __name__ == "__main__":
    data = load_youtube_data("TestData.json")
    print(data.level_1)
