import logging
import asyncio
import sys
from kademlia.network import Server
import random
import socket
import time


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    print("Local IP:", ip)
    s.close()
    return ip


LOCAL_IP = get_local_ip()

handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

NODE_NUM = 30
LIFETIME_MAX = 600  # second
LIFETIME_MIN = 550  # second
PORT_BASE = 9468
Node_Ports = []
Ports_Available = []


async def run():
    # getter server
    server_setter = Server()
    await server_setter.listen(8469)  # testing node port
    bootstrap_node_port = random.randint(PORT_BASE, PORT_BASE + NODE_NUM)
    bootstrap_node = (LOCAL_IP, bootstrap_node_port)
    await server_setter.bootstrap([bootstrap_node])

    # setter server
    server_getter = Server()
    await server_getter.listen(8470)  # testing node port
    bootstrap_node2_port = random.randint(PORT_BASE, PORT_BASE + NODE_NUM)
    if bootstrap_node2_port == bootstrap_node_port:
        bootstrap_node2_port = PORT_BASE
    bootstrap_node2 = (LOCAL_IP, bootstrap_node2_port)

    await server_getter.bootstrap([bootstrap_node2])

    success_count = 0
    total_count = 0
    starting_key = 1
    starting_value = 1
    for _ in range(100):

        await server_setter.set("key" + str(starting_key), "value" + str(starting_value))
        result = await server_getter.get("key" + str(starting_key))
        print("Get result:", result)
        if result == "value" + str(starting_value):
            success_count += 1

        # time.sleep(5)
        total_count += 1
        starting_key += 1
        starting_value += 1
    print(success_count / total_count)

    server_setter.stop()
    server_getter.stop()


asyncio.run(run())
