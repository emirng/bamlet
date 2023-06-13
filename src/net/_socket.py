import asyncio

class Socket:

    def __init__(self, inner : asyncio.streams.StreamWriter):
        if type(inner) != asyncio.streams.StreamWriter: raise TypeError()
        self._inner = inner

    def send(self, data):
        self._inner.write(data)

    def close(self):
        self._inner.close()
