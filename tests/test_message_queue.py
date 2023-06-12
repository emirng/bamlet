import asyncio
import pytest

@pytest.mark.timeout(0.1)
def test():
    from bamlet import MessageQueue

    stream = b"hi\nmr\nemirgn\n"
    mq = MessageQueue(stream) 

    for m in mq.get():
        if m == 'emirgn': break
    else:
        assert False

    assert mq.stream == b""

    mq.stream += b"karl\n"

    for m in mq.get():
        if m == 'karl': break
    else:
        assert False


@pytest.mark.asyncio
@pytest.mark.timeout(0.1)
async def test_async():
    from bamlet import MessageQueue

    stream = asyncio.streams.StreamReader()
    mq = MessageQueue(stream) 
    stream.feed_data(b"hi\nmr\nemirgn\n")

    async for m in mq.get_async():
        if m == 'emirgn': break
    else:
        assert False


