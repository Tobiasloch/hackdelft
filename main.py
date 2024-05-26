import argparse, json
from src.vehicle import Vehicle
from src.graph import generateGraph
from src.solver import solve
from src.render_map import render_map

ADDRESSFILE_KEY = "addressFile"
VEHICLE_KEY = "vehicles"

def main():

    parser = argparse.ArgumentParser(description="This program calculates the optimal routes for vehicles to deliver goods.")

    parser.add_argument("input_file", help="The input file containing the data for the problem. (JSON format)")
    
    optional_args_parser = parser.add_argument_group("Optional arguments")
    # parameter int k is optional
    optional_args_parser.add_argument("-k", "--k", type=int, default=4, help="The number of nearest neighbors to consider when building the k-NN graph. (Default: 4)")
    # solver args too
    optional_args_parser.add_argument("--greedy", action="store_true", default=True, help="Use the greedy algorithm to solve the problem.")
    optional_args_parser.add_argument("--exact", action="store_true", default=False, help="Use the exact algorithm to solve the problem.")
    optional_args_parser.add_argument("--dive", action="store_true", default=True, help="dive.")
    optional_args_parser.add_argument("--pricing_strategy", type=str, default="Hyper", help="The pricing strategy to use when solving the problem. (Default: Hyper)")
    optional_args_parser.add_argument("--time_limit", type=int, default=10, help="The time limit (in seconds) for the solver. (Default: 30)")

    args = parser.parse_args()

    input_file_path = args.input_file
    config = json.load(open(input_file_path, "r"))

    addresses = None
    if ADDRESSFILE_KEY in config:
        addresses = [line.strip().replace("\"", "") for line in open(config[ADDRESSFILE_KEY], "r")]
    else:
        print("No address file specified in input file.")
        return 1

    vehicles = None
    if VEHICLE_KEY in config:
        vehicles = []
        for vehicle_json in config[VEHICLE_KEY]:
            vehicle = Vehicle(**vehicle_json)
            vehicles.append(vehicle)
    else:
        print("No vehicles specified in input file.")
        return 1
    
    graph = generateGraph(addresses, vehicles, k=args.k)

    result = solve(graph, vehicles, greedy=args.greedy, exact=args.exact, pricing_strategy=args.pricing_strategy, time_limit=args.time_limit, dive=args.dive)
    
    for route_id, route in result.best_routes.items():
        route = [(graph.nodes[node]['address'], graph.nodes[node]['pos']) for node in result.best_routes[route_id]]
        vehicle = vehicles[result.best_routes_type[route_id]]
        name = f"{vehicle.name}_{vehicle.type}_{route_id}.html"
        render_map(route,name)
    

if __name__ == "__main__":
    main()