import argparse, json
from src.vehicle import Vehicle
from src.graph import generateGraph
from src.solver import solve
import pickle, os
from src.render_map import render_map

ADDRESSFILE_KEY = "addressFile"
VEHICLE_KEY = "vehicles"
HUBINDEX_KEY = "hubIndex"

def main():
    use_pickled_graph = True
    pickledump_new_graph = False
    parser = argparse.ArgumentParser(description="This program calculates the optimal routes for vehicles to deliver goods.")

    parser.add_argument("input_file", help="The input file containing the data for the problem. (JSON format)")
    
    optional_args_parser = parser.add_argument_group("Optional arguments")
    optional_args_parser.add_argument("--output_folder", type=str, default="out", help="The folder to save the route html files. (Default: out)")
    # parameter int k is optional
    
    solver_args_parser = optional_args_parser.add_argument_group("Solver options")
    solver_args_parser.add_argument("-k", "--k", type=int, default=4, help="The number of nearest neighbors to consider when building the k-NN graph. (Default: 4)")
    solver_args_parser.add_argument("--greedy", action="store_true", default=True, help="Use the greedy algorithm to solve the problem.")
    solver_args_parser.add_argument("--exact", action="store_true", default=False, help="Use the exact algorithm to solve the problem.")
    solver_args_parser.add_argument("--dive", action="store_true", default=True, help="dive.")
    solver_args_parser.add_argument("--pricing_strategy", type=str, default="Hyper", help="The pricing strategy to use when solving the problem. (Default: Hyper)")
    solver_args_parser.add_argument("--time_limit", type=int, default=10, help="The time limit (in seconds) for the solver. (Default: 30)")


    solver_args_parser.add_argument("--use_pickled_graph", action="store_true", default=False, help="Use the pickled graph.")
    solver_args_parser.add_argument("--pickledump_new_graph", action="store_true", default=False, help="Dump the new graph.")
    solver_args_parser.add_argument("--pickle_file_name", type=str, default="graph.pkl", help="The name of the pickle file to use.")


    args = parser.parse_args()

    input_file_path = args.input_file
    config = json.load(open(input_file_path, "r"))
    hubIndex = int(config[HUBINDEX_KEY]) if HUBINDEX_KEY in config else 0

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
    if args.use_pickled_graph == False:
        graph = generateGraph(addresses, vehicles, k=args.k, hubIndex=hubIndex)
        if args.pickledump_new_graph == True:
            with open(args.pickle_file_name, 'wb') as f:
                pickle.dump(graph, f)
    else:
        with open(args.pickle_file_name, 'rb') as f:
            graph = pickle.load(f)

    result = solve(graph, vehicles, greedy=args.greedy, exact=args.exact, pricing_strategy=args.pricing_strategy, time_limit=args.time_limit, dive=args.dive)
    
    os.makedirs(args.output_folder, exist_ok=True)
    for route_id, route in result.best_routes.items():
        route = [(graph.nodes[node]['address'], graph.nodes[node]['pos']) for node in result.best_routes[route_id]]
        vehicle = vehicles[result.best_routes_type[route_id]]
        path = f"{args.output_folder}/{vehicle.name}_{vehicle.type}_{route_id}.html"

        # generate an html file for the route using openstreetmap
        render_map(vehicle, route, path)
    
if __name__ == "__main__":
    main()