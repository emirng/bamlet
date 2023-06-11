import pytest
import asyncio
import time
import signal
from unittest.mock import patch


def test_import_and_init():
    from bamlet import Bamlet
    Bamlet()


@pytest.mark.timeout(1)
@pytest.mark.asyncio
@patch('bamlet.Bamlet.get_shutdown_signal_types', lambda self: [])
async def test_shutdown():
    from bamlet import Bamlet
    app = Bamlet()

    async def send_sigterm_after_delay(app,delay):
        await asyncio.sleep(delay)
        await app._shutdown()

    task_server = asyncio.create_task(app.run_async(host='localhost',port=5011))
    task_shutdowner = asyncio.create_task(send_sigterm_after_delay(app,0.1))

    await task_server
    await task_shutdowner
    assert not app.running
