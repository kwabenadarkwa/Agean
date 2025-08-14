import json
import os
import pathlib
import shutil
from os import walk
from typing import Union

from llist import sllist as linkedlist
from natsort import natsorted

from .constants import DEFAULT_CREATE_FILE_PROMPTS, DEFAULT_PROMPT_FILE
from .models import download_type, frame_split_type
from .models.prompt_data import (FileCreationPromptData,
                                 FrameExtractionPromptData)


def load_prompt_for_frame_parsing() -> FrameExtractionPromptData:
    with open(DEFAULT_PROMPT_FILE, "r") as f:
        data = json.load(f)
        return FrameExtractionPromptData(**data)


def load_prompt_data_for_file_creation() -> FileCreationPromptData:
    with open(DEFAULT_CREATE_FILE_PROMPTS, "r") as f:
        data = json.load(f)
        return FileCreationPromptData(**data)


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
