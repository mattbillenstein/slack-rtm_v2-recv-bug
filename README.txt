When listening on a websocket with the regular rtm_v2 lib using gevent, the
socket will after a time become unresponsive, and the cpu spin at 100%. This is
because the socket.recv() call doesn't return any data if the other end closed
the connection and the code gets into an infinite loop between _fetch and
receive because the error handling logic just returns an empty bytes object
- so the code whereever it is consuming data can't make progress.

Per the python3 sockets howto:

https://docs.python.org/3/howto/sockets.html:

    "When a recv returns 0 bytes, it means the other side has closed (or is in
    the process of closing) the connection. You will not receive any more data
    on this connection. Ever. You may be able to send data successfully..."

In this fix if we receive no data from sock.recv, just raise OSError so the
consuming code closes and establishes a new connecition.

You can run this code using the two requirements.txt - just connecting to slack
and waiting a time will cause this error to happen with the mainline lib.

  $ SLACK_BOT_TOKEN=... ./slack-bot.py

Tested on Python 3.10.4, Ubuntu 22.04 x86_64

Also, I might suggest replacing this code with the websocket-client lib (like
the async code uses the websockets lib) - it seems like a better implementation
of consuming data from websockets.
