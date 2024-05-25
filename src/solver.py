from networkx import Graph
from src.vehicle import Vehicle
from vrpy import VehicleRoutingProblem


def solve(graph:Graph, vehicles:list[Vehicle], greedy=False, exact=True, pricing_strategy="Hyper", time_limit=30) -> VehicleRoutingProblem:
    load_capacity = [vehicle.capacity for vehicle in vehicles]
    num_vehicles = [vehicle.count for vehicle in vehicles]
    
    prob = VehicleRoutingProblem(graph, mixed_fleet=True, load_capacity=load_capacity, num_vehicles=num_vehicles)
    return prob.solve(exact=exact,greedy=greedy,time_limit=time_limit,pricing_strategy=pricing_strategy)