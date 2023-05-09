# Networks-and-Mobile-Systems-Project

## Prerequisite
This Kademlia benchmark requires a working kademlia implementation which can be installed using the following: 
```
pip install kademlia
```
Find Kademlia installation location using 
```
pip list -v
```
Replace node.py and routing.py with our edited version

## Running Benchmark
In order to run the benchmark, first start the simulated Kademlia network: 
```
python3 create_nodes.py
```

Then, start the benchmark program: 
```
python3 set_get.py 
```
