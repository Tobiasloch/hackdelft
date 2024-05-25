import networkx
from src.vehicle import Vehicle

from sklearn.neighbors import kneighbors_graph
import numpy as np
import networkx as nx
import geolocator
from vrpy import VehicleRoutingProblem

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from google_interface import get_edge_weight

# Function to get coordinates
def get_coordinates(address):
    try:
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except GeocoderTimedOut:
        return get_coordinates(address)


def build_knn_graph(coordinates, k=3):
    """
    Build a k-NN graph from the given coordinates.

    Parameters:
    - coordinates (dict): A dictionary of address (key) to (latitude, longitude) (value).
    - k (int): The number of nearest neighbors.

    Returns:
    - G (networkx.Graph): The k-NN graph.
    """
    # Convert the coordinates to a NumPy array
    coordinates_list = list(coordinates.values())
    coords_array = np.array(coordinates_list)

    # Build the k-NN graph directly
    A = kneighbors_graph(coords_array, n_neighbors=k, mode='connectivity', include_self=False)

    # Convert the scipy sparse matrix to a networkx graph
    G = nx.from_scipy_sparse_array(A)

    # Add node attributes (address and position)
    for i, (address, (lat, lon)) in enumerate(coordinates.items()):
        G.nodes[i]['address'] = address
        G.nodes[i]['pos'] = (lat, lon)

    return G

def generateGraph(addresses: list[str], vehicles: list[Vehicle], k=3) -> networkx.Graph:
    # Get coordinates for each address
    coordinates = {address: get_coordinates(address) for address in addresses}
    G = build_knn_graph(coordinates, k)
    # Initialize the directed graph
    DG = nx.DiGraph()

    # Add nodes and their attributes from the undirected graph to the directed graph
    for node, data in G.nodes(data=True):
        if data['address'] != 'Mekelweg 4, 2628 CD Delft':
            DG.add_node(node, **data)


    # Add both directions for each edge in the undirected graph
    for u, v in G.edges:
        if G.nodes[u]['address'] != 'Mekelweg 4, 2628 CD Delft' and G.nodes[v]['address'] != 'Mekelweg 4, 2628 CD Delft':
            DG.add_edge(u, v)
            DG.add_edge(v, u)
    copy_node_data = G.nodes[0]
    new_outgoing_node = 'Source'
    new_incoming_node = 'Sink'
    DG.add_node(new_outgoing_node, **copy_node_data)
    DG.add_node(new_incoming_node, **copy_node_data)

    # Connect the new outgoing node to all existing nodes with outgoing edges
    for node in DG.nodes:
        if node != new_outgoing_node and node != new_incoming_node:
            DG.add_edge(new_outgoing_node, node)

    # Connect the new incoming node to all existing nodes with incoming edges
    for node in DG.nodes:
        if node != new_outgoing_node and node != new_incoming_node:
            DG.add_edge(node, new_incoming_node)
    
    # Initialize lists for origins and destinations
    origins = []
    destinations = []

    # Iterate through all edges
    for edge in DG.edges:
        origin, destination = edge
        origins.append(DG.nodes[origin]['pos'])
        destinations.append(DG.nodes[destination]['pos'])
    google_distances = get_edge_weight(origins, destinations)
    durations = [[trip['driving']['duration'], trip['bicycling']['duration']] for trip in google_distances]
    distances = [[trip['driving']['distance'], trip['bicycling']['distance']] for trip in google_distances]
    
    for node in DG.nodes:
        if node != 'Sink' and node != 'Source':
            DG.nodes[node]['demand'] = 1

    i = 0
    for u, v in DG.edges():
        DG.edges[u, v]['cost'] = durations[i]
        DG.edges[u, v]['distances'] = distances[i]
        i=i+1
    return DG