
class KBucket:
    def __init__(self, k):
        self.k = k
        self.nodes = []

    def add(self, node_id):
        if node_id not in self.nodes:
            if len(self.nodes) < self.k:
                self.nodes.append(node_id)
            else:
                self.nodes.pop(0)
                self.nodes.append(node_id)

    def find_closest(self, node_id, n=None):
        n = n or self.k
        sorted_nodes = sorted(self.nodes, key=lambda x: x.distance(node_id))
        return sorted_nodes[:n]
