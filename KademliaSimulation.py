import random
import asyncio
from kademlia.network import Server


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
    initial_node = Server()
    await initial_node.listen(8479)
    port = 8480
    for i in range(100):
        key = i
        value = Server()
        node_dict[key] = value
        await node_dict[key].listen(port, "192.168.1.233")
        await node_dict[key].bootstrap([("192.168.1.233", port-1)])
        port += 1
        await node_dict[key].set("key %s" % (key), "value %s" % (key))
    # print("Setting complete")
    # print(node_dict[0].retrieve_storage().values())
    # print(node_dict[0].bootstrappable_neighbors())

    # Simulate node churn
    churn_rate = 0.2  # Change the churn rate as needed
    churn_count = int(len(node_dict) * churn_rate)
    for _ in range(churn_count):
        churned_node_key = random.choice(list(node_dict.keys()))
        churned_node = node_dict.pop(churned_node_key)
        churned_node.stop()

    # Calculate success rate
    success_count = 0
    total_count = 0
    for i in range(100):
        try:
            result = await node_dict[0].get("key %s" % (i))
            if result == "value %s" % (i):
                success_count += 1
            total_count += 1
        except Exception as e:
            print("Error fetching value for key {}: {}".format(i, e))
            total_count += 1

    success_rate = success_count / total_count
    print("Success rate: {:.2f}".format(success_rate))

asyncio.run(run())
