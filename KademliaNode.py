import NodeID
import RoutingTable

class KademliaNode:
    def __init__(self, k=20):
        self.node_id = NodeID()
        self.routing_table = RoutingTable(k, self.node_id)
        self.data_store = {}


    def join(self, bootstrap_node):
        """
        The function is responsible for the process of a new node joining the Kademlia network. 

        Parameters:
            bootstrap_node: a known node in the existing network used as a starting point for the new node to join the network
        """
        
        # Add bootstrap node its routing table. This step helps establish an initial connection to the network.
        self.routing_table.add(bootstrap_node.node_id)

        # Perform a node lookup for its own node ID to discover more nodes
        self.find_node(self.node_id)


    def store(self, key, value):
        """
        The function to store a key-value pair in the Kademlia network.The node that wants to store the data will perform a "find_node" operation on the key to find the k nodes that are closest to the key. Then, the node will send "store" requests to those k closest nodes. The contacted nodes will store the key-value pair in their local data store.
        
        Parameters:
            key, value: key-value pair. 
        """
        
        target_node_id = NodeID(key)
        closest_nodes = self.routing_table.find_closest(target_node_id)

        # Normally, you would send STORE RPCs to the closest nodes
        # For simplicity, we simulate the process by storing data directly
        for node in closest_nodes:
            node.data_store[key] = value


    def lookup(self, key):
        """
        The function to retrieve the value associated with a given key from the Kademlia network. The node performs a search for the k closest nodes to the key and sends them a find value request. If any of these nodes have the requested value, they return it to the requesting node. 
  
        Parameters:
            key: the key associated with the value we want. 
          
        Returns:
            node.data_store[key]: the value associated with the given key, or None if we can't find it. 
        """
                
        target_node_id = NodeID(key)
        closest_nodes = self.routing_table.find_closest(target_node_id)

        # Normally, you would send FIND_VALUE RPCs to the closest nodes
        # For simplicity, we simulate the process by searching data directly
        for node in closest_nodes:
            if key in node.data_store:
                return node.data_store[key]

        return None

    
    def find_node(self, target_node_id):
        """
        The function to find a specific node with the given target_id or the k nodes that are closest to the target_id in the Kademlia network. Given a target node ID, the method returns a list of the k closest nodes to the target. This method is the basis for the node lookup process and is used in both the join and store operations. 
  
        Parameters:
            target_id: A NodeID object
        """

        closest_nodes = self.routing_table.find_closest(target_node_id)

        # Normally, you would send FIND_NODE RPCs to the closest nodes
        # For simplicity, we simulate the process by updating the routing table
        for node in closest_nodes:
            self.routing_table.add(node.node_id)
