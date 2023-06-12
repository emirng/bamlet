import asyncio
import pytest
import irc.bot
from irc.client import SimpleIRCClient
from bamlet import Bamlet

bot = None

class Bot( irc.bot.SingleServerIRCBot ):

    def __init__( self, nickname, server, port ):
        irc.bot.SingleServerIRCBot.__init__( self, [(server, port)], nickname, nickname )
        self.alive = True
        self.got_welcome = False


    def on_welcome( self, c, e ):
        self.got_welcome = True
        self.alive = False


    async def start( self ):
        self._connect()
        while self.alive:
            self.reactor.process_once()
            await asyncio.sleep( 0.1 )


async def start_bot():
    global bot
    bot = Bot( 'emirgn', 'localhost', 6667 )
    await bot.start()


@pytest.mark.asyncio
@pytest.mark.timeout(1)
async def test():
    from examples.example_002_irc.__main__ import main_async
    task_server = asyncio.create_task( main_async() )
    await asyncio.sleep( 0.2 ) # wait some time before start bot
    task_bot = asyncio.create_task( start_bot() )
    await task_bot
    Bamlet.app.shutdown()
    await task_server
    assert bot.got_welcome


