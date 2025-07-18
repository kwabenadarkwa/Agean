import json
import os
import shutil
from os import walk
from parser.flags_parser import args
from typing import Union

from llist import sllist as linkedlist
from natsort import natsorted

from models import download_type, frame_split_type, test_data
from models.test_data import YoutubeObject


def get_youtube_objects_based_on_level() -> list[YoutubeObject]:
    data = load_youtube_data(args.load_file)

    match args.level:
        case 1:
            return [youtube_object for youtube_object in data.level_1]
        case 2:
            return [youtube_object for youtube_object in data.level_2]
        case 3:
            return [youtube_object for youtube_object in data.level_3]
        case 4:
            return [youtube_object for youtube_object in data.level_4]
        case _:
            return [youtube_object for youtube_object in data.level_1]


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
    try:
        if isinstance(video, download_type.DownloaderReturnType) and os.path.exists(
            video.filepath
        ):
            os.remove(video.filepath)
        elif isinstance(
            video, frame_split_type.FrameSplitReturnType
        ) and os.path.exists(video.frames_path):
            shutil.rmtree(video.frames_path)

    except OSError as e:
        print("Error Removing file: %s - %s." % (e.filename, e.strerror))


if __name__ == "__main__":
    data = load_youtube_data("TestData.json")
    print(data.level_1)
