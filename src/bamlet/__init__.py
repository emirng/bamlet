from bamlet.app import Bamlet as Bamlet
from bamlet.message_queue import MessageQueue as MessageQueue
from bamlet.client import Client as Client

class Proxy:


    async def shutdown(self):
        await self.app._shutdown()

current_app = Proxy()

