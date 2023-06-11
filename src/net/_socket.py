import asyncio

class Socket:

    def __init__(self, client : asyncio.streams.StreamWriter):
        if type(client) != asyncio.streams.StreamWriter: raise TypeError()
        self._client = client

    def send(self, data):
        self._client.write(data)

    def close(self):
        self._client.close()
