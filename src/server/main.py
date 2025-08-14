import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from engine import async_api
from engine import YoutubeObject
# TODO: Fix engine imports - currently having issues with event_pipeline framework
from typing import Union

from fastapi import FastAPI

#TODO: engine could work if I just imported it as a package but I'll do that after I make sure that the server connection actually works
app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

