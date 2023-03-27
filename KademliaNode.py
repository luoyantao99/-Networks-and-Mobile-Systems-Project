import NodeID
import RoutingTable

class KademliaNode:
    def __init__(self, k=20):
        self.node_id = NodeID()
        self.routing_table = RoutingTable(k, self.node_id)
        self.data_store = {}

    def join(self, bootstrap_node):
        # TODO

    def store(self, key, value):
        # TODO

    def lookup(self, key):
        # TODO

    def find_node(self, target_id):
        # TODO
