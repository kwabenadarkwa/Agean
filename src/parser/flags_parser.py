import argparse
import pathlib

parser = argparse.ArgumentParser(description="Process event pipeline with flags")
parser.add_argument(
    "-l",
    "--level",
    type=int,
    default=1,
    help="Level of the type of videos the pipeline should process",
)

parser.add_argument(
    "-t",
    "--test-file",
    type=str,
    default="test_data.json",
    help="Select file to load data from",
)

parser.add_argument(
    "-p",
    "--prompt-file",
    type=str,
    default=str(pathlib.Path("prompts", "parse_prompts.json")),
    help="This file contains the prompts that will be used to generate the AI's response for the individual frames",
)

parser.add_argument(
    "-P",
    "--create-file-prompts",
    type=str,
    default=str(pathlib.Path("prompts", "create_file_prompts.json")), 
    help="This contains all the prompt that have to do with creation of the actual project file in the last stage of the pipeline",
) 
args = parser.parse_args()
