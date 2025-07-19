import argparse

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
    default="TestData.json",
    help="Select file to load data from",
)

parser.add_argument(
    "-p",
    "--prompt-file",
    type=str,
    default="Prompts.json",
    help="This file contains the prompts that will be used to generate the AI's response",
)

args = parser.parse_args()
