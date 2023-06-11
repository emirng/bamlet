import httpx
import asyncio
import pytest
from examples.example_003_http.__main__ import main_async
from bamlet import current_app


@pytest.mark.timeout(10)
@pytest.mark.asyncio
async def test():
    task_server = asyncio.create_task(main_async())

    
    await asyncio.sleep(1) # In case of issues try give server some time to start before moving on

    async with httpx.AsyncClient() as client:
        r = await client.get('http://localhost:8080/')
        assert r.status_code == 200

        with open('examples/example_003_http/index.html', 'rb') as f:
            assert f.read() == r.content

        r = await client.get('http://localhost:8080/file_that_does_not_exist')
        assert r.status_code == 404

    current_app.shutdown()
    await task_server
