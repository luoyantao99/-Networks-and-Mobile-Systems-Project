import random
import time
from KademliaNode import KademliaNode

def measure_latency(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    latency = end_time - start_time
    return result, latency

# Define the number of initial nodes, key-value pairs, and lookup operations
num_initial_nodes = 100
num_kv_pairs = 50
num_lookups = 100
churn_rate = 10
simulation_steps = 20

# Initialize the Kademlia network
nodes = [KademliaNode() for _ in range(num_initial_nodes)]

# Join the network
for i in range(1, num_initial_nodes):
    nodes[i].join(nodes[random.randint(0, i - 1)])

# Store some key-value pairs in the network
kv_pairs = {}
for _ in range(num_kv_pairs):
    # key = f'key{random.randint(1, 1000)}'
    # value = f'value{random.randint(1, 1000)}'
    key = random.randint(1, 1000)
    value = random.randint(1, 1000)
    kv_pairs[key] = value
    storing_node = random.choice(nodes)
    storing_node.store(key, value)

# Initialize performance metric counters
lookup_success_count = 0
lookup_failure_count = 0
total_latency = 0

# Simulation loop
for step in range(simulation_steps):
    print(f"Simulation step {step + 1}")

    # Perform churn by adding and removing nodes
    for _ in range(churn_rate):
        # Remove a random node
        removed_node = random.choice(nodes)
        nodes.remove(removed_node)

        # Add a new node
        new_node = KademliaNode()
        new_node.join(random.choice(nodes))
        nodes.append(new_node)

    # Perform lookup operations and measure performance
    for _ in range(num_lookups):
        key, expected_value = random.choice(list(kv_pairs.items()))
        lookup_node = random.choice(nodes)
        value, latency = measure_latency(lookup_node.lookup, key)
        total_latency += latency

        if value == expected_value:
            lookup_success_count += 1
        else:
            lookup_failure_count += 1

# Calculate and print performance metrics
success_rate = lookup_success_count / (lookup_success_count + lookup_failure_count)
average_latency = total_latency / (lookup_success_count + lookup_failure_count)

print(f"Success rate: {success_rate * 100}%")
print(f"Average lookup latency: {average_latency} seconds")
