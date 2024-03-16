from play_python.main import app
import pytest_asyncio
from async_asgi_testclient import TestClient
import asyncio
import pytest
import re


pytestmark = pytest.mark.asyncio(scope="module")
loop: asyncio.AbstractEventLoop

@pytest_asyncio.fixture(scope="module")
async def client():
    async with TestClient(app) as ac:
        yield ac

async def test_stream_err(client: TestClient):
    endpoint = "/stream-err"
    response = await client.get(endpoint, stream=True)
    async for res in response.__aiter__():
        res = res.decode("utf-8")
        print(res)
        assert re.match(r"\d+ \/ \d+ \(\d+\.\d+%\)", res) or res == ""

async def test_stream_ok(client: TestClient):
    endpoint = "/stream-ok"
    response = await client.get(endpoint, stream=True)
    async for res in response.__aiter__():
        res = res.decode("utf-8")
        print(res)
        assert re.match(r"\d+ \/ \d+ \(\d+\.\d+%\)", res) or res == ""

