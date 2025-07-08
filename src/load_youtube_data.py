import json

from pydantic import BaseModel


class YoutubeObject(BaseModel):
    link: str
    ide: str
    theme: str
    duration: str


class TestData(BaseModel):
    level_1: list[YoutubeObject]
    level_2: list[YoutubeObject]
    level_3: list[YoutubeObject]
    level_4: list[YoutubeObject]


def load_youtube_data(file_name: str) -> TestData:
    with open(file_name, "r") as f:
        data = json.load(f)
        return TestData(**data)


if __name__ == "__main__":
    data = load_youtube_data("TestData.json")
    print(data.level_1)
