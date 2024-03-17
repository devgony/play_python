from typing import Callable, Optional
from fastapi import FastAPI  
from fastapi.responses import StreamingResponse
import asyncio
from starlette.middleware.cors import CORSMiddleware
from starlette_context.middleware import ContextMiddleware
from starlette_context.plugins.forwarded_for import ForwardedForPlugin
from time import sleep

app = FastAPI()   

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.add_middleware(
    ContextMiddleware,
    plugins={ForwardedForPlugin()}
)

async def mock_aync_generator(async_sleep: Optional[Callable] = None):
    await asyncio.sleep(1) # should do some slow async logics

    total = 5
    for current in range(1, total + 1):

        sleep(1) # should do some slow sync logics

        progress = f"{current} / {total} ({current / total * 100}%)"
        print(f">>> rigt before yield: {progress}")
        yield progress

        if async_sleep is not None:
            await async_sleep()

async def async_sleep():
    await asyncio.sleep(0.01)

@app.get("/stream-err")
async def stream_err():
    return StreamingResponse(mock_aync_generator(), media_type="text/event-stream")

@app.get("/stream-ok")
async def stream_ok():
    return StreamingResponse(mock_aync_generator(async_sleep), media_type="text/event-stream")

