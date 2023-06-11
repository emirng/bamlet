import asyncio
from bamlet import Bamlet



app = Bamlet()

@app.handle_client()
async def handle_client(client, message_queue):

    while True:

        print(client)
        for message in message_queue:
            print(message) 

        await asyncio.sleep(0.4) 
    


def main():
    app.run('localhost', 8080)

async def main_async():
    await app.run_async('localhost', 8080)


if __name__ == "__main__":
    main()


