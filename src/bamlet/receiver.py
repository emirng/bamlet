class Receiver:

    def __init__( self, stream ):
        self.stream = stream

    async def __call__( self ):
        return await self.stream.read( 256 )


