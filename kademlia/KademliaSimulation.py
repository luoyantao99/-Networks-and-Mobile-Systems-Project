from itertools import count
import random
import asyncio
from kademlia.network import Server
import socket
import threading
import keyboard
import time


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    print("Local IP:", ip)
    s.close()
    return ip


def get_local_ip_mac():
    return "0.0.0.0"


async def create_and_bootstrap_node(port, bootstrap_node):
    node = Server()
    await node.listen(port)
    await node.bootstrap(bootstrap_node)
    return node


async def set_key_value(node, key, value):
    await node.set(key, value)


async def get_value(node, key):
    return await node.get(key)


def get_random_node(nodes):
    return random.choice(list(nodes.values()))


def get_random_key():
    return "key {}".format(random.randint(1, 100))


async def run():
    node_dict = {}
    initial_node_num = 100
    initial_node = Server()
    await initial_node.listen(8479)
    # ip = get_local_ip()
    ip = get_local_ip_mac()
    port = 8480

    # initial
    for i in range(initial_node_num):
        '''key for node_dict and port can be the same, to reduce further calculation'''
        key = port
        value = Server()
        node_dict[key] = value
        await node_dict[key].listen(port, ip)

        # choose random node as bootstrap node
        random_bootstrap_node = random.randint(8479, port - 1)
        await node_dict[key].bootstrap([(ip, random_bootstrap_node)])
        port += 1
        await node_dict[key].set("key %s" % (key), "value %s" % (key))
    # print("Setting complete")
    # print(node_dict[0].retrieve_storage().values())
    # print(node_dict[0].bootstrappable_neighbors())

    global esc
    global cal_rate

    count = 0

    # global starting_port
    churn_starting_port = port

    # Change the period as needed to change churn rate
    churn_period_in_second = 15

    while True:
        # Simulate node churn
        async def concurrent_churn(port):
            if len(node_dict) == 0:
                print("No node survived")
                return

            # out
            churned_node_key = random.choice(list(node_dict.keys()))
            churned_node = node_dict.pop(churned_node_key)
            churned_node.stop()
            print("node out")

            # in
            key = port
            print("node in, key:", key)
            value = Server()
            node_dict[key] = value
            await node_dict[key].listen(port, ip)
            random_bootstrap_node = random.choice(list(node_dict.keys()))
            await node_dict[key].bootstrap([(ip, random_bootstrap_node)])
            port += 1
            await node_dict[key].set("key %s" % (key), "value %s" % (key))

        async def call_concurrent_churn(churn_starting_port):

            # several churn running concurrently, mimicing churning serveral nodes in 1 second
            await asyncio.gather(concurrent_churn(churn_starting_port + 1), concurrent_churn(churn_starting_port + 2), concurrent_churn(churn_starting_port + 3), concurrent_churn(churn_starting_port + 4))

        # record the time
        start_time = time.time()

        await call_concurrent_churn(churn_starting_port)

        # make sure that port number increased properly to avoid conflict
        concurrent_churn_number = 4
        churn_starting_port = churn_starting_port + concurrent_churn_number

        # record the time
        end_time = time.time()

        # check if sleep is needed
        time.sleep(max(churn_period_in_second - (end_time - start_time), 0))

        print("node num:", len(node_dict))

        print(count, len(node_dict))
        count += 1

        if esc:
            print("User pressed ESC")
            break

        if cal_rate:  # Calculate success rate
            print("Calculate success rate")
            success_count = 0
            total_count = 0

            for i in range(initial_node_num):
                total_count += 1
                try:
                    result = await node_dict[0].get("key %s" % (i))
                    if result == "value %s" % (i):
                        success_count += 1
                        print(result)
                except Exception as e:
                    print("Error fetching value for key {}: {}".format(i, e))

            success_rate = success_count / total_count
            print("Success rate: {:.2f}".format(success_rate))
            cal_rate = False


# User input
esc = False
cal_rate = False


def KeyboardListener_esc():
    global esc
    keyboard.wait('esc')
    esc = True


def KeyboardListener_success():
    global cal_rate
    keyboard.wait('s')
    cal_rate = True


t1 = threading.Thread(target=KeyboardListener_esc)
t1.start()
t2 = threading.Thread(target=KeyboardListener_success)
t2.start()


asyncio.run(run())

t1.join()
t2.join()
