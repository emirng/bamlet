class MessageQueue():

    def __init__( self, stream, separator = b'\n', encoding='utf-8'):
        self.stream = stream
        self.separator = separator
        self.encoding = encoding


    def get(self):
        sep = self.separator
        while True:
            if sep in self.stream:
                r = self.stream[:self.stream.find(sep)]
                del self.stream[:self.stream.find(sep)+len(sep)]
                yield r.decode()
            else:
                break


    async def get_async(self):
        while True:
            r = await self.stream.readuntil( self.separator )
            r = r[:-len(self.separator)]
            yield r.decode()


