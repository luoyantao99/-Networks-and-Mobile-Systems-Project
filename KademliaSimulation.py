from KademliaNode import KademliaNode
import time
import numpy as np
import random
from collections import defaultdict

class KademliaSimulation:
    def __init__(self, churn_rates, num_nodes=100, num_iterations=100, k=20):
        self.churn_rates = churn_rates
        self.num_nodes = num_nodes
        self.num_iterations = num_iterations
        self.k = k
        self.nodes = []

    def run(self):
        results = defaultdict(lambda: defaultdict(list))
        for churn_rate in self.churn_rates:
            print(f"Running simulation for churn rate {churn_rate}")
            for _ in range(self.num_iterations):
                self.initialize_nodes()
                self.simulate_churn(churn_rate)
                success_rate, latency, avg_routing_table_size = self.measure_performance()
                results[churn_rate]["success_rate"].append(success_rate)
                results[churn_rate]["latency"].append(latency)
                results[churn_rate]["avg_routing_table_size"].append(avg_routing_table_size)
        return results

    def initialize_nodes(self):
        self.nodes = [KademliaNode() for _ in range(self.num_nodes)]
        bootstrap_node = self.nodes[0]
        for node in self.nodes[1:]:
            node.join_network(bootstrap_node)

    def simulate_churn(self, churn_rate):
        churned_nodes = set(random.sample(self.nodes, int(churn_rate * self.num_nodes)))
        for node in churned_nodes:
            self.nodes.remove(node)
            for remaining_node in self.nodes:
                remaining_node.routing_table.remove(node)

    def measure_performance(self):
        num_queries = 0
        num_successes = 0
        total_latency = 0
        total_routing_table_size = 0

        for node in self.nodes:
            for _ in range(5):  # 5 queries per node
                num_queries += 1

                closest_nodes, target_id = None, None
                target_node = node.get_random_node()
                if target_node:
                    target_id = target_node.get_id()
                start_time = time.perf_counter()

                if target_id:
                    closest_nodes = node.find_node(target_id)

                latency = time.perf_counter() - start_time
                total_latency += latency

                if closest_nodes and target_node in closest_nodes:
                    num_successes += 1
            # for bucket in node.routing_table.buckets:
            #     print(bucket.all_bucket_nodes())
            # print()
            total_routing_table_size += sum(len(bucket.all_bucket_nodes()) for bucket in node.routing_table.buckets)

        success_rate = num_successes / num_queries
        avg_latency = total_latency / num_queries
        avg_routing_table_size = total_routing_table_size / len(self.nodes)

        return success_rate, avg_latency, avg_routing_table_size


churn_rates = [0.1, 0.25, 0.5, 0.75]
simulation = KademliaSimulation(churn_rates)
results = simulation.run()

for churn_rate in churn_rates:
    print(f"Churn rate {churn_rate}:")
    print(f"  - Average query success rate: {np.mean(results[churn_rate]['success_rate'])}")
    print(f"  - Average lookup latency: {np.mean(results[churn_rate]['latency'])} seconds")
    # print(f"  - Average routing table size: {np.mean(results[churn_rate]['avg_routing_table_size'])}")
