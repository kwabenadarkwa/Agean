import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
# TODO: Fix engine imports - currently having issues with event_pipeline framework
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from engine import YoutubeObject, async_api

# TODO: engine could work if I just imported it as a package but I'll do that after I make sure that the server connection actually works
app = FastAPI()


class ExtractCodeRequest(BaseModel):
    video_url: str
    title: str = "API Video"
    duration: str = "Unknown"
    frame_extraction_fps: int = 1
    duplicate_removal_threshold: float = 0.8
    level: int = 1


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/extract_code")
async def extract_code(request: ExtractCodeRequest):
    try:
        youtube_obj = YoutubeObject(
        #
            title=request.title, link=request.video_url, duration=request.duration
        )

        result = await async_api.extract_code_async(
            youtube_object=[youtube_obj],
            frame_extraction_fps=request.frame_extraction_fps,
            duplicate_removal_threshold=request.duplicate_removal_threshold,
            level=request.level,
        )

        return {
            "status": "success",
            "result": result,
            "video_info": {
                "url": request.video_url,
                "title": request.title,
                "duration": request.duration,
            },
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "video_url": request.video_url}
