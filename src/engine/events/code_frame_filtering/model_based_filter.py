"""
Model-based code frame filtering using pre-trained neural networks.

This module implements the model-based approach for filtering non-code frames
from video sequences using a pre-trained machine learning model.
"""

import pathlib
from typing import Tuple, cast

import cv2 as cv
import keras
import numpy as np
from event_pipeline.base import EventBase
from keras.models import Model
from keras.preprocessing.image import load_img
from llist import sllist as linkedlist

from ... import constants
from ... import utils
from ...models import frame_split_type


class RemoveNonCodeFramesWithModel(EventBase):
    """
    Event processor that removes non-code frames using a pre-trained ML model.
    
    This class uses a pre-trained neural network model to classify frames as
    containing code or not. The model was originally from PS2CODE but has been
    noted to have lower accuracy than the rule-based approach.
    """
    
    def process(self) -> Tuple[bool, frame_split_type.FrameSplitReturnType]:
        """
        Process video frames using ML model to filter out non-code frames.
        
        Returns:
            Tuple of (success_flag, filtered_frame_info)
        """
        video_frames_info_obj: frame_split_type.FrameSplitReturnType = (
            self.previous_result.first().content  # type:ignore
        )
        
        try:
            model = cast(
                Model, keras.models.load_model(constants.ML_MODEL_PATH, compile=False)
            )
            assert model is not None, f"Failed to load model from {constants.ML_MODEL_PATH}"

            images = self.load_images_as_np_array(video_frames_info_obj)
            predictions = model.predict(images)
            
            # Filter frames based on model predictions
            filtered_frames = self._filter_frames_by_predictions(
                video_frames_info_obj, predictions
            )
            
            video_frames_info_obj.frame_names = filtered_frames
            
            return True, video_frames_info_obj
            
        except Exception as e:
            print(f"Error in model-based filtering: {e}")
            return False, video_frames_info_obj

    def _filter_frames_by_predictions(
        self,
        video_frames_info_obj: frame_split_type.FrameSplitReturnType,
        predictions: np.ndarray,
        threshold: float = 0.5
    ) -> linkedlist:
        """
        Filter frames based on model predictions.
        
        Args:
            video_frames_info_obj: Frame split information object
            predictions: Model predictions for each frame
            threshold: Classification threshold (default 0.5)
            
        Returns:
            Filtered linked list containing only code frames
        """
        filtered_frames = linkedlist()
        names = utils.load_frame_names(video_frames_info_obj)
        
        frame = names.first
        frame_idx = 0
        code_frame_count = 0
        
        while frame is not None and frame_idx < len(predictions):
            if predictions[frame_idx] > threshold:
                filtered_frames.append(frame.value)
                code_frame_count += 1
                
            frame = frame.next
            frame_idx += 1
            
        print(f"Model filtered {code_frame_count}/{len(predictions)} frames as code frames")
        return filtered_frames

    @staticmethod
    def load_images_as_np_array(
        video_frames_info_obj: frame_split_type.FrameSplitReturnType,
    ) -> np.ndarray:
        """
        Load all images as numpy array for model input.
        
        Converts all frame images to numpy arrays with the target size expected
        by the ML model. This preprocessing step is crucial for model inference.

        Args:
            video_frames_info_obj: Frame split object containing frame information.

        Returns:
            Numpy array of preprocessed images ready for model input.
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
    def remove_non_code_frames_based_on_classification():
        """Legacy method - kept for compatibility."""
        pass
