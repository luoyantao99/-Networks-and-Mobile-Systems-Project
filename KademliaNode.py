import hashlib
import random

class KBucket:
    def __init__(self, k=20):
        self.k = k
        self.nodes = []

    def all_bucket_nodes(self):
        return self.nodes

    def one_bucket_nodeIDs(self):
        nodeID_list = []
        for node in self.nodes:
            nodeID_list.append(node.id)
        return nodeID_list

    def add(self, node):
        if node not in self.nodes:
            if len(self.nodes) < self.k:
                self.nodes.append(node)
            else:
                return False
        return True

    def remove(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            return True
        return False

    def __len__(self):
        return len(self.nodes)

class RoutingTable:
    def __init__(self, k=20, id_bits=160):
        self.k = k
        self.id_bits = id_bits
        self.buckets = [KBucket(k) for _ in range(id_bits)]

    def add(self, node):
        bucket_index = self.get_bucket_index(node.id)
        return self.buckets[bucket_index].add(node)

    def remove(self, node):
        bucket_index = self.get_bucket_index(node.id)
        return self.buckets[bucket_index].remove(node)

    def find_closest_nodes(self, target_id):
        bucket_index = self.get_bucket_index(target_id)

        # if target ID is found in the caller node's bucket, which means exact hit
        if self.buckets[bucket_index].one_bucket_nodeIDs() and target_id in self.buckets[bucket_index].one_bucket_nodeIDs():
            for node in self.buckets[bucket_index].nodes:
                if node.id == target_id:
                    return [node]

        # else, get the closest K nodes that has closest distance to the target id
        all_nodes = []
        for bucket in self.buckets:
            all_nodes.extend(bucket.all_bucket_nodes())
        return sorted(all_nodes, key=lambda n: n.distance_to(target_id))[:self.k]

    def get_bucket_index(self, node_id):
        return self.id_bits - node_id.bit_length()

    def get_random_node(self):
        '''get a random node for query success rate testing'''
        all_nodes = []
        for i in range(len(self.buckets)):
            all_nodes.extend(self.buckets[i].all_bucket_nodes())
        if not all_nodes:
            return None
        return random.choice(all_nodes)


class KademliaNode:
    def __init__(self, id=None, k=20):
        if id is None:
            id = random.getrandbits(160)
        self.id = id
        self.k = k
        self.routing_table = RoutingTable(k)
        self.storage = {}

    def get_id(self):
        return self.id

    def ping(self, target_id):
        pass

    def store(self, key, value):
        self.storage[key] = value

    def retrieve(self, key):
        return self.storage.get(key)

    def distance_to(self, other_id):
        return self.id ^ other_id

    def find_node(self, target_id):
        return self.routing_table.find_closest_nodes(target_id)

    def find_value(self, target_id):
        pass

    def join_network(self, bootstrap_node):
        self.routing_table.add(bootstrap_node)
        bootstrap_node.find_node(self.id)

    def get_random_node(self):
        return self.routing_table.get_random_node()

def hash_function(value):
    return int(hashlib.sha1(value.encode()).hexdigest(), 16)



