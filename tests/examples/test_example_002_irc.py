import asyncio
import pytest
import irc.bot
from examples.example_002_irc import main
from irc.client import SimpleIRCClient

# TODO: try patch instead
async def start(self):
    await self.reactor.process_forever()
SimpleIRCClient.start = start
# ---

class Bot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)

    async def on_welcome(self, c, e):
        self.got_welcome = True

# async wrapper
async def f():
    bot = Bot('x', 'emil', 'localhost', 9999)
    bot.start()

@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test():
    task_server = asyncio.create_task(main())
    await asyncio.sleep(1) # wait a second before connect bot
    task_bot = asyncio.create_task(f())
    await task_bot
    await task_server

    assert bot.got_welcome

