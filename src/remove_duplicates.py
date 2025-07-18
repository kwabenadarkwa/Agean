import pathlib
from os import walk
from typing import Tuple

import cv2 as cv
import numpy as np
from event_pipeline.base import EventBase
from llist import sllist as linkedlist
from natsort import natsorted

import frame_split

FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann = cv.FlannBasedMatcher(index_params, search_params)  # type: ignore


class RemoveDuplicates(EventBase):
    def process(
        self, duplicate_removal_threshold: float = 0.8, *args, **kwargs
    ) -> Tuple[bool, linkedlist]:
        """This function removes duplicate frames from a video by comparing the SIFT
        features of each frame.

        Args:
            video_frames (frame_split.FrameSplitReturnType): The video frames to remove
            duplicates from.
            threshold (float, optional): The threshold for the SIFT feature comparison.
            Defaults to 0.8.

        Returns:
            linkedlist: The linked list of frame names with duplicates removed.

        Raises:
            FileNotFoundError: If a frame cannot be loaded.
            ValueError: If the SIFT descriptors cannot be computed for one or both frames.
        """
        sift = cv.SIFT_create()
        video_frames: frame_split.FrameSplitReturnType = self.previous_result[0]
        frame_names = load_frame_names(video_frames)
        # print(frame_names)

        reference = frame_names.first
        while reference is not None and reference.next is not None:
            try:
                reference_img = cv.imread(
                    str(pathlib.Path(video_frames.frames_path, reference.value))
                )
                if reference_img is None:
                    raise FileNotFoundError(
                        f"Cannot load frame: {str(pathlib.Path(video_frames.frames_path, reference.value))}"
                    )
                gray_reference_img = cv.cvtColor(reference_img, cv.COLOR_BGR2GRAY)

                next_compare_img = cv.imread(
                    str(pathlib.Path(video_frames.frames_path, reference.next.value))
                )
                if next_compare_img is None:
                    raise FileNotFoundError(
                        f"Cannot load frame: {str(pathlib.Path(video_frames.frames_path, reference.next.value))}"
                    )
                gray_next_compare_img = cv.cvtColor(next_compare_img, cv.COLOR_BGR2GRAY)

                _, des1 = sift.detectAndCompute(gray_reference_img, None)
                _, des2 = sift.detectAndCompute(gray_next_compare_img, None)

                if des1 is None or des2 is None:
                    raise ValueError(
                        "SIFT descriptors could not be computed for one or both frames"
                    )

                matches = flann.knnMatch(des1, des2, k=2)
                print(f"Number of matches: {len(matches)}")
                good_count = 0

                for m, n in matches:
                    if m.distance < duplicate_removal_threshold * n.distance:
                        good_count += 1

                matches_beyond_threshold = (
                    good_count / len(matches) > duplicate_removal_threshold
                )
                if matches_beyond_threshold:
                    print("there was a match somewhere")
                    node_to_remove = reference.next
                    frame_names.remove(node_to_remove)
                    # INFO: can't use this because llist internally won't make it work
                    # it is just going to use it even if it is removed from the list
                    # reference.next = reference.next.next
                else:
                    reference = reference.next

            except Exception as e:
                print(f"Error processing frame {reference.value}: {e}")
                reference = reference.next

        print("Done removing duplicates")
        print(frame_names)
        return frame_names


def load_frame_names(video_frames: frame_split.FrameSplitReturnType) -> linkedlist:
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


if __name__ == "__main__":
    pass
