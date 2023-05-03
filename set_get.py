import logging
import asyncio
import socket
import time
from kademlia.network import Server
import random


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    print("Local IP:", ip)
    s.close()
    return ip


LOCAL_IP = get_local_ip()


handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

async def Set(port, key, value):
    server = Server()
    await server.listen(8469)
    bootstrap_node = (LOCAL_IP, port)
    await server.bootstrap([bootstrap_node])
    await server.set(key, value)
    server.stop()


async def Get(port, key):
    server = Server()
    await server.listen(8469)
    bootstrap_node = (LOCAL_IP, port)
    await server.bootstrap([bootstrap_node])

    result = await server.get(key)
    print("Get result:", result)
    server.stop()
    return result

# asyncio.run(Set(9477, "aa", "bb"))

# print("===================================================")

# print(asyncio.run(Get(9487, "aa")))


NODE_NUM = 30
PORT_BASE = 9468

TEST_ROUND = 10
ROUND_INTERVAL = 10 # second

total_get_time = 0
success_count = 0
get_time = []

for count in range(TEST_ROUND):
    print("+++> Round: {}".format(count))

    key = "key" + str(count)
    value = "value" + str(count)
    setport = random.randint(PORT_BASE, PORT_BASE + NODE_NUM)

    asyncio.run(Set(setport, key, value))

    # sleep after setting
    time.sleep(ROUND_INTERVAL)

    getport = random.randint(PORT_BASE, PORT_BASE + NODE_NUM)

    getter_start_time = time.time()
    result = asyncio.run(Get(getport, key))
    getter_end_time = time.time()

    get_time.append(getter_end_time - getter_start_time)
    total_get_time += getter_end_time - getter_start_time

    if result == value:
        success_count += 1

    #time.sleep(ROUND_INTERVAL)


print("success:{}, total:{}, success rate:{:.2f}%".format(success_count, TEST_ROUND, success_count / TEST_ROUND * 100.))
print("get time:", get_time)
print("total get time:{}, average get time:{}".format(total_get_time, total_get_time / TEST_ROUND))


