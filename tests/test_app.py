import pytest
import asyncio

def test_import_and_init():
    from bamlet import Bamlet
    Bamlet()


@pytest.mark.asyncio
@pytest.mark.timeout(1)
async def test_shutdown():
    from bamlet import Bamlet
    app = Bamlet()

    async def call_shutdown_after_delay( app, delay ):
        await asyncio.sleep( delay )
        app.shutdown()

    async def start_server():
        try:
            await app.run_async( 'localhost', 5011 )
        except asyncio.exceptions.CancelledError:
            pass

    task_server = asyncio.create_task( start_server() )
    task_shutdowner = asyncio.create_task( call_shutdown_after_delay( app, 0.1 ) )

    await task_server
    await task_shutdowner

    # no need for asserts, if test come this far it means that it been (most likely) shut down
