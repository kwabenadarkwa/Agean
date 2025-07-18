from pydantic import BaseModel

from models import download_type, frame_split_type


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


