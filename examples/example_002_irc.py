import asyncio
from bamlet import Bamlet


async def main():

    app = Bamlet()

    @app.handle_client()
    async def handle_client(client):

        while True:
            mq = list(client.message_queue)
            for message in mq:
                message = message.strip()

                if message.startswith("USER"):
                    username = message.split(' ')[1]
                    await client.send(
                        ":localhost 001 {0} :Welcome to the Localhost, {0}".format(username))

            await client.send("PING :10A45D9F")


            await asyncio.sleep(2)

    await app.run_async(host="localhost", port=9999)

if __name__ == '__main__':
    #main() # TODO: we need to resolve test first then see how we can run this with or without async
    pass
