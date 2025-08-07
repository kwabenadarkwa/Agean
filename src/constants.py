import pathlib

model_name = "weights.h5"
model_folder_name = "MLModels"
ML_MODEL_PATH = pathlib.Path(
    pathlib.Path(__file__).parent, model_folder_name, model_name
)
VIDEOS_PATH = "videos"
TESTING_VIDEOS_PATH = "testExtractedFrames"
MODEL_IMAGE_TARGET_SIZE = (300, 300)
