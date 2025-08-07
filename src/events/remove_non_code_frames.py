import pathlib
from typing import Tuple

import cv2 as cv
import keras
from keras.models import Model
import numpy as np
from event_pipeline.base import EventBase
from keras.preprocessing.image import load_img
from llist import sllist as linkedlist
from typing import cast 

import constants
import utils
from models import frame_split_type


class RemoveNonCodeFrames(EventBase):
    def process(self) -> Tuple[bool, frame_split_type.FrameSplitReturnType]:
        video_frames_info_obj: frame_split_type.FrameSplitReturnType = (
            self.previous_result.first().content  # type:ignore
        )

        model = cast(Model, keras.models.load_model(constants.ML_MODEL_PATH, compile=False)) 
        assert model is not None, f"Failed to load model from {constants.ML_MODEL_PATH}"

        images = self.load_images_as_np_array(video_frames_info_obj) 
        prediction = model.predict(images) 
        print(prediction) 
        return True, video_frames_info_obj 

    @staticmethod
    def load_images_as_np_array(
        video_frames_info_obj: frame_split_type.FrameSplitReturnType,
    ) -> np.ndarray:
        """
        Loads all the images in the video frames info object as a numpy array of images that are converted to their respective
        numpy array representations.
        This is important because the model expects a numpy array of images as input.

        Args:
            video_frames_info_obj (frame_split_type.FrameSplitReturnType):
            The frame split object that contains the information about the frames in the video.

        Returns:
            np.ndarray: A numpy array of images that are converted to their respective numpy array representations.
        """
        names: linkedlist = utils.load_frame_names(video_frames_info_obj)
        assert names is not None, "Failed to load frame names" 
        path_to_folder_for_video = video_frames_info_obj.frames_path
        images = []

        frame = names.first
        while frame is not None:
            frame_path = str(pathlib.Path(path_to_folder_for_video, frame.value))

            try:
                images.append(
                    np.array(
                        load_img(
                            frame_path, target_size=constants.MODEL_IMAGE_TARGET_SIZE
                        )
                    )
                )
            except Exception as e:
                print(f"Error converting frame {frame.value}: {e}")

            frame = frame.next
        return np.array(images)

    @staticmethod
    def remove_non_code_frames_based_on_prediction():
        pass
