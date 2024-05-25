from sklearn.neighbors import kneighbors_graph
import networkx as nx
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import numpy as np

# Initialize Nominatim API
geolocator = Nominatim(user_agent="hackathon")


# Function to get coordinates
def get_coordinates(address):
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
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
        G.nodes[i]['pos'] = (lon, lat)

    return G


def plot_knn_graph(G):
    """
    Plot the k-NN graph using networkx and matplotlib.

    Parameters:
    - G (networkx.Graph): The k-NN graph to plot.
    """
    pos = nx.get_node_attributes(G, 'pos')
    labels = nx.get_node_attributes(G, 'address')

    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=300, node_color='red', font_size=8, font_color='black', labels=labels)
    plt.title(f'k-Nearest Neighbors Graph')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()


def distance(coord1, coord2):
    """
    Calculate the Euclidean distance between two coordinates.

    Parameters:
    - coord1 (tuple): The first coordinate (lat1, lon1).
    - coord2 (tuple): The second coordinate (lat2, lon2).

    Returns:
    - dist (float): The Euclidean distance between the two coordinates.
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return np.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)


def build_example_graph():
    # List of addresses
    addresses = [
        "Mekelweg 4, 2628 CD Delft",
        "Markt 87, 2611 GS Delft",
        "Olof Palmestraat 1, 2616 LN Delft",
        "Troelstralaan 71, 2624 ET Delft",
        "Kleveringweg 2, 2616 LZ Delft",
        "Schieweg 15L, 2627 AN Delft",
        "Westeinde 2A, 2275 AD Voorburg",
        "Herenstraat 101, 2271 CC Voorburg",
        "Haags Kwartier 55, 2491 BM Den Haag",
        "Spui 70, 2511 BT Den Haag",
        "Liguster 202, 2262 AC Leidschendam"
    ]

    # Get coordinates for each address
    coordinates = {address: get_coordinates(address) for address in addresses}

    # Print the coordinates
    for address, coord in coordinates.items():
        print(f"Address: {address} => Coordinates: {coord}")

    # Build the k-NN graph
    k = 4  # Number of neighbors
    G = build_knn_graph(coordinates, k)

    G = G.to_directed()

    G.add_edge("Source", 4, distance=0)
    G.add_edge(4, "Sink", distance=0)

    G.nodes["Source"]['pos'] = G.nodes[4]['pos']
    G.nodes["Sink"]['pos'] = G.nodes[4]['pos']

    for v in G.nodes:
        if v in ["Source", "Sink"]:
            continue
        G.nodes[v]['demand'] = 1
        G.add_edge(v, "Sink")
        G.add_edge("Source", v)

    for (u, v) in G.edges:
        G.edges[u, v]['distance'] = distance(G.nodes[u]['pos'], G.nodes[v]['pos']) * 1000

    return G
