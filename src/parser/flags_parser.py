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
    "-f",
    "--load-file",
    type=str,
    default="TestData.json",
    help="Select file to load data from",
)

args = parser.parse_args()
