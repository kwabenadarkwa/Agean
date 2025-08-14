from pydantic import BaseModel


class YoutubeObject(BaseModel):
    link: str
    ide: str | None = None
    title: str
    theme: str | None = None
    duration: str


