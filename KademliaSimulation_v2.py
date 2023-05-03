import logging
import asyncio
import sys
from kademlia.network import Server
import random
import socket
import time

'''log handler'''
# handler = logging.StreamHandler()
# formatter = logging.Formatter(
#     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# log = logging.getLogger('kademlia')
# log.addHandler(handler)
# log.setLevel(logging.DEBUG)


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    print("Local IP:", ip)
    s.close()
    return ip


LOCAL_IP = get_local_ip()


NODE_NUM = 30  # number of nodes and port for bootstrap purposes
PORT_BASE = 9468

port = 8469  # port for the setter and getter


async def run(starting_key, starting_value):
    print("Starting Getter")
    # getter server
    server_setter = Server()
    await server_setter.listen(port)  # testing node port
    bootstrap_node_port = random.randint(PORT_BASE, PORT_BASE + NODE_NUM)
    bootstrap_node = (LOCAL_IP, bootstrap_node_port)
    await server_setter.bootstrap([bootstrap_node])

    print("Starting Setter")
    # setter server
    server_getter = Server()
    await server_getter.listen(port + 1)  # testing node port
    bootstrap_node2_port = random.randint(PORT_BASE, PORT_BASE + NODE_NUM)
    if bootstrap_node2_port == bootstrap_node_port:
        bootstrap_node2_port = PORT_BASE
    bootstrap_node2 = (LOCAL_IP, bootstrap_node2_port)

    await server_getter.bootstrap([bootstrap_node2])

    print("Starting Setting Job")
    await server_setter.set("key" + str(starting_key), "value" + str(starting_value))
    asyncio.sleep(10)
    print("Starting Getting Job")
    getter_start_time = time.time()
    result = await server_getter.get("key" + str(starting_key))
    getter_end_time = time.time()

    time_for_getting = (getter_end_time - getter_start_time)

    print("Get result: ", result)
    matched = False
    if result == "value" + str(starting_value):
        matched = True

    print("Time for getter: ", str(time_for_getting))
    server_setter.stop()
    server_getter.stop()
    return matched, time_for_getting


success_count = 0
total_count = 5
starting_key = 1
starting_value = 1
total_latency = 0
# job for running
for _ in range(total_count):
    matched, time_for_getting = asyncio.run(run(starting_key, starting_value))
    starting_key = starting_key + 1
    starting_value = starting_value + 1
    if matched:
        success_count += 1
    total_latency += time_for_getting

print("The success rate for getting the correct value is: ",
      success_count / total_count)
print("The average latency is: ", total_latency / total_count)
