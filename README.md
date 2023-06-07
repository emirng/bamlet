# ![hamlet2](https://github.com/emirng/bamlet/assets/135670768/dee90c39-5f3d-48bb-be60-abc632ea3556) bamlet
Also think it is too much code just to set up a simple TCP-server. Wish there were something just a easy as Flask but more closer to clean TCP. Hopefully bamlet can save your day.

![b](https://github.com/emirng/bamlet/actions/workflows/main.yml/badge.svg)

```python
# an example of a TCP-server that answers with pong if you message ping to it

from bamlet import Bamlet

app = Bamlet()

@app.on_message(delimiter='\n')
def on_message(message):
    if message == "ping":
        return "pong"
    return ""

app.run(host="localhost", port=5011)
```

## Examples
This project comes with some examples. 

To run an example execute this command in to project's top folder
```
python3 -m examples.example_001_on_message
```



## API

| Class | Description |
|----------|-------------|
| `Bamlet` | The server. |
| `Client` | A client that is connected (or disconnected) to the server. |
| `MessageQueue` | A helper that helps retrive "messages" from a client. |

### Bamlet

| Method | Arguments | Description |
|----------|-------------|---|
| `run` | host, port | Will start the server.  |
| `run_async` | host, port | Will start the server asynchronously  |

### Client

| Method | Arguments | Description |
|----------|-------------|---|
| `send` | text | Sends a message to the client  |

#### MessageQueue

Does not have any method but if used as an iterable it will yield complete messages in the queue

