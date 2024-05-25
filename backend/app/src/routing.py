import networkx as nx
import matplotlib.pyplot as plt
from vrpy import VehicleRoutingProblem


if __name__ == "__main__":

    G = nx.DiGraph()
    G.add_edge("Source", 1, cost=[1, 2])
    G.add_edge("Source", 2, cost=[2, 4])
    G.add_edge(1, "Sink", cost=[0, 0])
    G.add_edge(2, "Sink", cost=[2, 4])
    G.add_edge(1, 2, cost=[1, 2])

    # nx.draw(G, with_labels=True)
    # plt.show()

    prob = VehicleRoutingProblem(G, mixed_fleet=True, load_capacity=[10, 15])
    prob.solve()
