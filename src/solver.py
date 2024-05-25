from networkx import Graph
from src.vehicle import Vehicle
from vrpy import VehicleRoutingProblem


def solve(graph:Graph, vehicles:list[Vehicle]) -> dict[str, list[tuple[int]]]:
    prob = VehicleRoutingProblem(Graph, mixed_fleet=True, load_capacity=[10, 5], num_vehicles=[1, 4])#, drop_penalty=0.1)
    prob.solve(exact=True,greedy=False,time_limit=30,pricing_strategy='Hyper')
    pass