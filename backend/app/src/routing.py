import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from vrpy import VehicleRoutingProblem

def cost(distance): 
    car_cost = distance * 0.5
    bike_cost = distance * 0.7
    return [car_cost, bike_cost]

# Create graph
G = nx.DiGraph()
for v in [1, 2, 3, 4, 5]:
    G.add_edge("Source", v, cost=cost(10))
    G.add_edge(v, "Sink", cost=cost(10))
G.add_edge(1, 2, cost=cost(10))
G.add_edge(2, 3, cost=cost(10))
G.add_edge(3, 4, cost=cost(15))
G.add_edge(4, 5, cost=cost(10))

for v in G.nodes():
    if v not in ["Source", "Sink"]:
        G.nodes[v]["demand"] = 1

prob = VehicleRoutingProblem(G, mixed_fleet=True, load_capacity=[3, 2], num_vehicles=[1, 4])#, drop_penalty=10000)
prob.solve()

print(f"{prob.best_value=}")
print(f"{prob.best_routes=}")
print(f"{prob.best_routes_load=}")
print(f"{prob.best_routes_type=}")


nx.draw(G, with_labels=True)
plt.show()