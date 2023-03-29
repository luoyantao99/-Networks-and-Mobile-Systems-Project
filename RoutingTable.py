from KBucket import KBucket
from collections import deque

class RoutingTable:
    def __init__(self, k, node_id):
        self.k = k
        self.node_id = node_id
        self.buckets = [KBucket(k) for _ in range(160)]

    def add(self, node_id):
        bucket_index = self._find_bucket_index(node_id)
        self.buckets[bucket_index].add(node_id)

    def _find_bucket_index(self, node_id):
        return node_id.distance(self.node_id).bit_length() - 1

    def find_closest(self, node_id, n=None):
        n = n or self.k
        bucket_index = self._find_bucket_index(node_id)
        closest_nodes = deque(self.buckets[bucket_index].find_closest(node_id, n))

        # Expand search to other buckets if necessary
        left, right = bucket_index - 1, bucket_index + 1
        while len(closest_nodes) < n and (left >= 0 or right < 160):
            if left >= 0:
                closest_nodes.extend(self.buckets[left].find_closest(node_id, n))
                left -= 1
            if right < 160:
                closest_nodes.extend(self.buckets[right].find_closest(node_id, n))
                right += 1

        return list(closest_nodes)[:n]
