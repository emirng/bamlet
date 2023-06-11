import asyncio
import pytest
from net import Net

response = None

async def echo_client():
    global response
    msg = 'echo this!'
    await asyncio.sleep( 0.1 )
    reader, writer = await asyncio.open_connection( 'localhost', 9001 )
    writer.write( msg.encode() )
    await writer.drain()
    response_in_bytes = await reader.read(len(msg))
    response = response_in_bytes.decode()
    writer.close()
    await writer.wait_closed()
    Net.net.shutdown()

@pytest.mark.asyncio
@pytest.mark.timeout(5)
async def test():
    from examples.example_004_net import main_async
    task_server = asyncio.create_task( main_async() )
    task_client = asyncio.create_task( echo_client() )

    await task_server
    await task_client

    assert response == 'echo this!'


