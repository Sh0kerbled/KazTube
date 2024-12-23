from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import os
import aiofiles

app = FastAPI()

directory = "D:/Games/project/AA/video"

def get_video_list():
    return [{"id": idx, "name": file} for idx, file in enumerate(os.listdir(directory))]

video_list = get_video_list()

@app.get("/videos")
async def list_videos():
    return video_list

# files = os.listdir(directory)

# videoList = [
#     files
# ]

# @app.get("/test")
# async def test():
#     return files

# @app.get("/sosal")
# async def test() -> list:
#     return videoList

# @app.get("/sosal/{id}")
# async def test(id: int) -> dict:
#     for video in videoList:
#         if video['id'] == id:
#             return video
        
#     raise HTTPException(status_code=404,detail="video not found")

