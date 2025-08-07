import json
import os
import pathlib
import shutil
from os import walk
from parser.flags_parser import args
from typing import Union

from llist import sllist as linkedlist
from natsort import natsorted

from models import download_type, frame_split_type, test_data
from models.prompt_data import PromptData
from models.test_data import YoutubeObject


def get_test_videos_level() -> int:
    return args.level


def get_youtube_objects_based_on_level() -> list[YoutubeObject]:
    """This function returns a list of YoutubeObjects based on the level of the test.
    Args:

    Returns:
        list[YoutubeObject]: The list of YoutubeObjects based on the level of the test.
    """
    data = load_youtube_data()

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


def load_youtube_data() -> test_data.TestData:
    with open(args.test_file, "r") as f:
        data = json.load(f)
        return test_data.TestData(**data)


# TODO: this could possible be abstracted into a better function
def load_prompt_data() -> PromptData:
    with open(args.prompt_file, "r") as f:
        data = json.load(f)
        return PromptData(**data)


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


def remove_all_old_frames(path_to_frames, paths: linkedlist) -> None:
    path = paths.first
    while path is not None:
        remove_thing_based_on_type(str(pathlib.Path(path_to_frames, path.value)))
        path = path.next


def remove_after_failure(path) -> None:
    shutil.rmtree(path)


def remove_thing_based_on_type(
    remove_item: Union[
        download_type.DownloaderReturnType, frame_split_type.FrameSplitReturnType, str
    ],
) -> None:
    try:
        if isinstance(
            remove_item, download_type.DownloaderReturnType
        ) and os.path.exists(remove_item.filepath):
            os.remove(remove_item.filepath)
        elif isinstance(remove_item, str):
            os.remove(remove_item)
        elif isinstance(
            remove_item, frame_split_type.FrameSplitReturnType
        ) and os.path.exists(remove_item.frames_path):
            shutil.rmtree(remove_item.frames_path)
    except OSError as e:
        print("Error Removing file: %s - %s." % (e.filename, e.strerror))
