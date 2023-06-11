# an example of a TCP-server that answers with pong if you message ping to it

from bamlet import Bamlet
app = Bamlet()

@app.on_message(delimiter='\n')
def on_message(message):
    if message == "ping":
        return "pong\n"
    if message == "marco":
        return "polo\n"
    return "?\n"

app.run(host="localhost", port=5011)
