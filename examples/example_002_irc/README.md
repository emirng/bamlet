# Example 002 IRC

This show how one could use bamlet to write an IRC-server. Do not expect this IRC-server to have all the functionalities as normal IRC-server, I am pretty certain it doesn't. This is just a proof of concept.

## How to run IRC-server
Run this from projects root folder
```
$ python -m examples.example_002_irc
```

Expected output
```
 * Serving bamlet app
 * Running on localhost:6667
 ```
## How to connect to it and its functionalities
For these steps I use a clean install of Pidgin. Hopefully any IRC-client would work just as well.

### Connect

Connect to localhost port 6667 (6667 should be the default port for any IRC-client). Add IRC-account. Pick any username you want.

![image](https://github.com/emirng/bamlet/assets/135670768/25ff02ab-2896-4c84-9f4b-c9a663f22a60)

![image](https://github.com/emirng/bamlet/assets/135670768/1d2af61a-11f7-4e84-b42b-90b61b593e76)

After being added Pidgin should auto-connect it. If you see a green circle with Available next to it, it should been connected.

### Add bamlet as Buddy

This IRC-server has a bot on it called bamlet. Try add it as a Buddy. If your IRC-client does not support "Buddies" just try message user bamlet directly.

![image](https://github.com/emirng/bamlet/assets/135670768/51db0c2e-8ca2-4b26-b67b-ef7471e19fd3)

Try message it something. It will give send something back. See screenshot below for spoiler.

![image](https://github.com/emirng/bamlet/assets/135670768/65001aae-0508-48b2-b97b-08e4a42e93ea)
