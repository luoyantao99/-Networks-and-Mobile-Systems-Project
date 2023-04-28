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

# async def create_and_bootstrap_node(port, bootstrap_node):
#     node = Server()
#     await node.listen(port)
#     await node.bootstrap(bootstrap_node)
#     return node


# async def set_key_value(node, key, value):
#     await node.set(key, value)


# async def get_value(node, key):
#     return await node.get(key)


# def get_random_node(nodes):
#     return random.choice(list(nodes.values()))


# def get_random_key():
#     return "key {}".format(random.randint(1, 100))


async def run():
    node_dict = {}
    initial_node_num = 100
    initial_node = Server()
    await initial_node.listen(8479)
    ip = get_local_ip()
    port = 8480

    # initial
    for i in range(initial_node_num):
        key = i
        value = Server()
        node_dict[key] = value
        await node_dict[key].listen(port, ip)
        await node_dict[key].bootstrap([(ip, port-1)])
        port += 1
        await node_dict[key].set("key %s" % (key), "value %s" % (key))
    # print("Setting complete")
    # print(node_dict[0].retrieve_storage().values())
    # print(node_dict[0].bootstrappable_neighbors())

    churn_rate = 0.2  # Change the churn rate as needed
    churn_count = int(len(node_dict) * churn_rate)

    global esc
    global cal_rate

    count = 0
    while True:
        # Simulate node churn
        for _ in range(churn_count):
            if len(node_dict) == 0:
                print("No node survived")
                return

            if random.choice([0,1]) == 0: # out
                print("node out")
                churned_node_key = random.choice(list(node_dict.keys()))
                churned_node = node_dict.pop(churned_node_key)
                churned_node.stop()

            '''
            if random.choice([0,1]) == 1: # in
                key = len(node_dict)
                print("node in, key:", key)
                if key < initial_node_num - 1:
                    value = Server()
                    node_dict[key] = value
                    await node_dict[key].listen(port, ip)
                    await node_dict[key].bootstrap([(ip, port-1)])
                    port += 1
                    await node_dict[key].set("key %s" % (key), "value %s" % (key))
                else:
                    print("node capacity full")
            
            print("node num:", len(node_dict))
            '''

        # time.sleep(1)

        print(count, len(node_dict))
        count += 1
        
        if esc:
            print("User pressed ESC")
            break

        if cal_rate: # Calculate success rate
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

        if count == 1:
            print("End.")
            break


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
