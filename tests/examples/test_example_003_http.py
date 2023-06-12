import asyncio
import pytest
import httpx
from bamlet import Bamlet


@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test():
    from examples.example_003_http.__main__ import main_async

    task_server = asyncio.create_task( main_async() )
    
    await asyncio.sleep(0.1) # In case of issues try give server some time to start before moving on

    async with httpx.AsyncClient() as client:

        # verify that index page work
        r = await client.get('http://localhost:8080/')
        assert r.status_code == 200
        with open('examples/example_003_http/index.html', 'rb') as f:
            assert f.read() == r.content

        # verify that 404 work on a page not existing
        r = await client.get('http://localhost:8080/file_that_does_not_exist')
        assert r.status_code == 404

    Bamlet.app.shutdown()

    await task_server


