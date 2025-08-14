import pathlib

#TODO: remember to move the weights.h5 file to the ml_models folder outside of the src folder when you're done
model_name = "weights.h5"
model_folder_name = "ml_models"
ML_MODEL_PATH = pathlib.Path(
    pathlib.Path(__file__).parent, model_folder_name, model_name
)
VIDEOS_PATH = "videos"
TESTING_VIDEOS_PATH = "test_extracted_frames"
MODEL_IMAGE_TARGET_SIZE = (300, 300)
