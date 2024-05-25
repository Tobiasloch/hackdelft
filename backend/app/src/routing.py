from vrpy import VehicleRoutingProblem
from graph import build_example_graph, plot_knn_graph


def cost(distance):
    car_cost = distance * 0.5
    bike_cost = distance * 0.7
    return [car_cost, bike_cost]


G = build_example_graph()

for (u, v) in G.edges:
    G.edges[u, v]['cost'] = cost(G.edges[u, v]['distance'])

for (u, v) in G.edges:
    print(f"{u=}, {v=}, {G.edges[u, v]['cost'] = }")

plot_knn_graph(G)

prob = VehicleRoutingProblem(G, mixed_fleet=True, load_capacity=[8, 6], num_vehicles=[1, 4])#, drop_penalty=0.1)
prob.solve(time_limit=5.0)

print(f"{prob.best_value=}")
print(f"{prob.best_routes=}")
print(f"{prob.best_routes_load=}")
print(f"{prob.best_routes_type=}")
