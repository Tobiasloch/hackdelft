from typing import Union
import requests

def process_list(addresses: list, name: str) -> str:
    """Processes a list of addresses."""
    if type(addresses[0]) == list or type(addresses[0]) == tuple:  # Assume multiple origins and destinations
        # Iterate through the list of destinations and build the URL
        addrs = f'{name}='
        for addr in addresses:
            addrs += f'{addr[0]}%2C{addr[1]}%7C'
        addrs = addrs.rstrip('%7C')  # Remove the trailing '%7C'
    else:  # Assume single origin and destination
        addrs = f'{name}={addresses[0]}%2C{addresses[1]}%7C'
        addrs = addrs.rstrip('%7C')  # Remove the trailing '%7C'
    return addrs

def build_url(destinations: Union[list, list[list]], origins: Union[list, list[list]], mode: Union[str, list[str]] = 'driving', return_type: str = 'matrix') -> Union[str, list[str]]:
    """Builds the URL for the Google Maps API request.
    Args:
        destinations: The destination(s) for the request.
        origins: The origin(s) for the request.
        mode: The mode of transportation for the request. Can be a single mode or a list of modes. Must be a subset of 'driving', 'bicycling'.
        return_type: The type of return value. Can be 'matrix' or 'list'. If 'matrix', the function will return a single URL string. If 'list', the function will return a list of URL strings.
    Returns:
        url: The URL(s) for the API request for the specified mode(s). If only one mode is specified, the list will only have one element. The type of the return value depends on the return_type parameter.
    """

    base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    units = 'units=metric'
    # Google Maps API Key
    with open('API_KEY.txt', 'r') as f:
        key = f'key={f.read()}'  # Read the API key from a text file

    # Handle single point input by converting it to a list of one point
    if isinstance(destinations[0], (int, float)):
        destinations = [destinations]
    if isinstance(origins[0], (int, float)):
        origins = [origins]

    if type(mode) == str:  # Single mode
        if return_type == 'matrix':
            dests = process_list(destinations, 'destinations')
            origs = process_list(origins, 'origins')
            return f'{base_url}{dests}&{origs}&{units}&{key}&mode={mode}'
        elif return_type == 'list':
            urls = []
            for origin, destination in zip(origins, destinations):
                orig = f'origins={origin[0]}%2C{origin[1]}'
                dest = f'destinations={destination[0]}%2C{destination[1]}'
                urls.append(f'{base_url}{dest}&{orig}&{units}&{key}&mode={mode}')
            return urls
    else:  # Multiple modes
        urls = []
        for origin, destination in zip(origins, destinations):
            for m in mode:
                orig = f'origins={origin[0]}%2C{origin[1]}'
                dest = f'destinations={destination[0]}%2C{destination[1]}'
                urls.append(f'{base_url}{dest}&{orig}&{units}&{key}&mode={m}')
        return urls

def fetch_data_from_api(urls: Union[str, list[str]]) -> Union[dict, list[dict]]:
    """Fetches data from the API given a single URL or a list of URLs.
    Args:
        urls: A single URL or a list of URLs.
    Returns:
        responses: A dictionary or a list of dictionaries containing the API responses.
    """
    if isinstance(urls, str):
        urls = [urls]

    responses = []
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            responses.append(response.json())
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as err:
            print(f"Error occurred: {err}")

    return responses if len(responses) > 1 else responses[0]

def transform_responses(responses: list[dict], origins: list[tuple], destinations: list[tuple], modes: list[str]) -> list[dict]:
    """Transforms the API responses into the desired format.
    Args:
        responses: A list of dictionaries containing the API responses.
        origins: A list of origin coordinates.
        destinations: A list of destination coordinates.
        modes: A list of transportation modes used in the requests.
    Returns:
        transformed: A list of dictionaries in the desired format.
    """
    transformed = []
    response_idx = 0
    for origin, destination in zip(origins, destinations):
        combined_response = {}
        for mode in modes:
            response = responses[response_idx]
            response_idx += 1
            if response['rows'][0]['elements'][0]['status'] == 'OK':
                combined_response[mode] = {
                    'duration': response['rows'][0]['elements'][0]['duration']['value'],
                    'distance': response['rows'][0]['elements'][0]['distance']['value']
                }
            else:
                combined_response[mode] = {'duration': None, 'distance': None}
        transformed.append(combined_response)
    return transformed

def get_edge_weight(origins: list[tuple], destinations: list[tuple]) -> dict:
    """Get the edge weight (distance) between two points.
    Args:
        origin: The origin coordinates.
        destination: The destination coordinates.
    Returns:
        edge_weight: A dictionary containing the distance and duration between the two points.
    """
    modes = ['driving', 'bicycling']
    urls = build_url(destinations, origins, modes, return_type='list')
    responses = fetch_data_from_api(urls)
    edge_weight = transform_responses(responses, origins, destinations, modes)
    return edge_weight

def __main__():
    # Test the function with multiple points
    origins = [(52.0115073, 4.358595), (52.0115073, 4.358595)]
    destinations = [(52.0266492, 4.3624455), (51.9973499, 4.3512313)]

    print(get_edge_weight(origins, destinations))

if __name__ == '__main__':
    __main__()
