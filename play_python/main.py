from typing import Callable, Optional
from fastapi import FastAPI  
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()   

async def mock_aync_generator(sleep: Optional[Callable] = None):
    for i in range(1, 11):
        progress = f"{i} / 10 ({i/10*100}%)"
        print(f">>> progress: {progress}")
        yield progress
        if sleep is not None:
            await sleep()

async def sleep():
    await asyncio.sleep(0.01)

@app.get("/stream-err")
async def stream_err():
    return StreamingResponse(mock_aync_generator(), media_type="text/event-stream")

@app.get("/stream-ok")
async def stream_ok():
    return StreamingResponse(mock_aync_generator(sleep), media_type="text/event-stream")

