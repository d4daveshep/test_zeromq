"""Example using zmq with asyncio coroutines"""
# Copyright (c) PyZMQ Developers.
# This example is in the public domain (CC-0)

import asyncio
import json
import time

import zmq
from zmq.asyncio import Context, Poller

url = 'tcp://127.0.0.1:5555'

ctx = Context.instance()


async def ping() -> None:
    """print dots to indicate idleness"""
    while True:
        await asyncio.sleep(0.1)
        print('.')


# async def receiver() -> None:
#     """receive messages with polling"""
#     pull = ctx.socket(zmq.PULL)
#     pull.connect(url)
#     poller = Poller()
#     poller.register(pull, zmq.POLLIN)
#     while True:
#         events = await poller.poll()
#         if pull in dict(events):
#             print("recving", events)
#             msg = await pull.recv_multipart()
#             print('recvd', json.loads(msg[0].decode("utf-8")))


async def sender() -> None:
    """send a message every second"""
    tic = time.time()
    push = ctx.socket(zmq.PUSH)
    push.bind(url)
    while True:
        time_elapsed = time.time() - tic
        string_to_send = json.dumps({"time-elapsed": time_elapsed})
        print(f"sending = {string_to_send}")
        await push.send_multipart([string_to_send.encode("utf-8")])
        await asyncio.sleep(1)


asyncio.run(
    asyncio.wait(
        [
            # ping(),
            # receiver(),
            sender(),
        ]
    )
)
