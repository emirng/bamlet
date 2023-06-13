import asyncio
from bamlet import Bamlet

app = Bamlet()

@app.handle_client()
async def handle_client(client, message_queue):
    async for message in message_queue.get_async():
        print(message) 


def main():
    app.run( 'localhost', 5022 )


async def main_async():
    try:
        await app.run_async( 'localhost', 5022 )
    except asyncio.exceptions.CancelledError:
        pass


if __name__ == '__main__':
    main()


