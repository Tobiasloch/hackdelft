import networkx
from src.vehicle import Vehicle

from sklearn.neighbors import kneighbors_graph
import numpy as np
import networkx as nx
import geolocator

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

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

def generateGraph(addresses: list[str], vehicles: list[Vehicle]) -> networkx.Graph:
    pass