import pathlib
from typing import Tuple

import bounding_box_detector_pkg as bbox
import cv2 as cv
from event_pipeline.base import EventBase

import utils
from models import frame_split_type


class CropFrames(EventBase):
    def process(self) -> Tuple[bool, frame_split_type.FrameSplitReturnType]:
        bounding_box_details: bbox.BoundingBoxReturnType = (
            self.previous_result.first().content  # type:ignore
        )

        video_frames_details_obj: frame_split_type.FrameSplitReturnType = (
            bounding_box_details.returnType
        )
        x1, y1, x2, y2 = (
            bounding_box_details.x1,
            bounding_box_details.y1,
            bounding_box_details.x2,
            bounding_box_details.y2,
        )
        frame_names = utils.load_frame_names(video_frames_details_obj)

        reference = frame_names.first
        while reference is not None and reference.next is not None:
            try:
                file_path = str(
                    pathlib.Path(
                        video_frames_details_obj.frames_path,
                        reference.value,
                    )
                )

                reference_img = cv.imread(file_path)
                if reference_img is None:
                    raise FileNotFoundError(
                        f"Cannot load frame: {str(pathlib.Path(video_frames_details_obj.frames_path, reference.value))}"
                    )
                else:
                    crop_img = reference_img[y1:y2, x1:x2]
                    utils.remove_thing_based_on_type(file_path)
                    print("image get's cropped")
                    cv.imwrite(file_path, crop_img)
                reference = reference.next

            except Exception as e:
                print(f"Error processing frame {reference.value}: {e}")
                reference = reference.next
        return True, video_frames_details_obj
