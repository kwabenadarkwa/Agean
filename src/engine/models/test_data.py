from pydantic import BaseModel


class YoutubeObject(BaseModel):
    link: str
    ide: str
    title: str
    theme: str
    duration: str


