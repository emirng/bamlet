# an example of a TCP-server that answers with pong if you message ping to it

import asyncio
from bamlet import Bamlet

app = Bamlet()

@app.on_message()
def on_message(message):
    if message == 'ping':
        return 'pong'

def main():
    app.run( 'localhost', 5011 )


async def main_async():
    try:
        await app.run_async( 'localhost', 5011 )
    except asyncio.exceptions.CancelledError:
        pass


if __name__ == '__main__':
    main()


