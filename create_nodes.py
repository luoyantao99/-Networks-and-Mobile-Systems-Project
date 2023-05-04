import asyncio
import random
import socket
import time
import multiprocessing
from kademlia.network import Server
import numpy as np


NODE_NUM = 100
LIFETIME_AVG = 180  # second
PORT_BASE = 9468


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    # print("Local IP:", ip)
    s.close()
    return ip


LOCAL_IP = get_local_ip()


def create_node(Ports_Available, Node_Ports):
    port = Ports_Available[0]

    lock.acquire()
    Ports_Available.remove(port)
    Node_Ports.append(port)
    lock.release()

    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)

    loop = asyncio.get_event_loop()
    server = Server()
    #print("port->", port)
    loop.run_until_complete(server.listen(port))

    lifetime = random.randint(LIFETIME_AVG*0.9, LIFETIME_AVG*1.1)

    print("Created a node on port:{}, life time:{}".format(port, lifetime))

    try:
        loop.run_until_complete(asyncio.sleep(lifetime))
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()

        server = None
        loop = None

        lock.acquire()
        Node_Ports.remove(port)
        Ports_Available.append(port)
        lock.release()

        print("Node {} exited after {} seconds".format(port, lifetime))
        # print(Node_Ports)
        # print(Ports_Available)



def connect_node(Ports_Available, Node_Ports):
    lock.acquire()
    if len(Ports_Available) == 0:
        lock.release()
        return

    port = random.choice(Ports_Available)
    neighbor = random.choice(Node_Ports)

    Ports_Available.remove(port)
    Node_Ports.append(port)
    lock.release()

    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)

    loop = asyncio.get_event_loop()
    server = Server()
    #print("port->", port, "connect->", neighbor)
    loop.run_until_complete(server.listen(port))

    bootstrap_node = (LOCAL_IP, neighbor)
    loop.run_until_complete(server.bootstrap([bootstrap_node]))

    lifetime = int(np.random.normal(LIFETIME_MAX, LIFETIME_MAX/10))

    print("Created a node on port:{}, connect to:{}, life time:{}".format(port, neighbor, lifetime))

    try:
        loop.run_until_complete(asyncio.sleep(lifetime))
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()

        lock.acquire()
        Node_Ports.remove(port)
        Ports_Available.append(port)
        lock.release()

        print("Node {} exited after {} seconds".format(port, lifetime))


lock = multiprocessing.Lock()


def main():
    Node_Ports = multiprocessing.Manager().list()
    Ports_Available = multiprocessing.Manager().list()

    # initial
    for i in range(NODE_NUM):
        Ports_Available.append(i + PORT_BASE)

    t1 = multiprocessing.Process(target=create_node, args=(Ports_Available, Node_Ports))
    t1.start()

    while len(Node_Ports) == 0:
        time.sleep(1)

    while True:
        t2 = multiprocessing.Process(target=connect_node, args=(Ports_Available, Node_Ports))
        t2.start()

        time.sleep(2)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
