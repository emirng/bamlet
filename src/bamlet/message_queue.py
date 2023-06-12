class MessageQueue():

    def __init__( self, stream, separator = b'\n', encoding='utf-8'):
        self.stream = stream
        self.separator = separator
        self.encoding = encoding


    def get(self):
        while True:
            if b'\n' in self.stream:
                r = self.stream[:self.stream.find(b'\n')]
                self.stream = self.stream[self.stream.find(b'\n')+1:]
                yield r.decode()
            else:
                break


    async def get_async(self):
        while True:
            r = await self.stream.readuntil( self.separator )
            r = r[:-len(self.separator)]
            yield r.decode()


