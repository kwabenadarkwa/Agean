import pathlib
from pathlib import Path

# TODO: remember to move the weights.h5 file to the ml_models folder outside of the src folder when you're done
model_name = "weights.h5"
model_folder_name = "ml_models"
ML_MODEL_PATH = pathlib.Path(
    pathlib.Path(__file__).parent, model_folder_name, model_name
)
VIDEOS_PATH = "videos"
TESTING_VIDEOS_PATH = "test_extracted_frames"
MODEL_IMAGE_TARGET_SIZE = (300, 300)

# CLI defaults for server mode
DEFAULT_LEVEL = 1
DEFAULT_TEST_FILE = str(pathlib.Path(Path(__file__).parent / "test_data.json"))
DEFAULT_PROMPT_FILE = str(
    pathlib.Path(Path(__file__).parent / "prompts" / "parse_prompts.json")
)
DEFAULT_CREATE_FILE_PROMPTS = str(
    pathlib.Path(Path(__file__).parent / "prompts" / "create_file_prompts.json")
)
