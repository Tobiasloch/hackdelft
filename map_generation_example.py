import folium

# Dictionary of addresses and their corresponding coordinates
coordinates = {
    "Mekelweg 4, 2628 CD Delft": (51.9988441, 4.3736485),
    "Markt 87, 2611 GS Delft": (52.0115073, 4.358595),
    "Olof Palmestraat 1, 2616 LN Delft": (52.0127665, 4.3811469),
    "Troelstralaan 71, 2624 ET Delft": (51.9973499, 4.3512313),
    "Kleveringweg 2, 2616 LZ Delft": (52.0266492, 4.3624455),
    "Schieweg 15L, 2627 AN Delft": (51.9948117, 4.3667978),
    "Westeinde 2A, 2275 AD Voorburg": (52.0648646, 4.3626176),
    "Herenstraat 101, 2271 CC Voorburg": (52.0672856, 4.3636863),
    "Haags Kwartier 55, 2491 BM Den Haag": (52.0627222, 4.3819389),
    "Spui 70, 2511 BT Den Haag": (52.0779773, 4.3169084),
    "Liguster 202, 2262 AC Leidschendam": (52.0877886, 4.3833151),
}

# Create a map centered around Delft
map_center = (52.0115073, 4.358595)  # Centered on one of the coordinates
mymap = folium.Map(location=map_center, zoom_start=13)

# Add markers for each address
for address, coord in coordinates.items():
    folium.Marker(
        location=coord,
        popup=address,
    ).add_to(mymap)

# Add edges between consecutive addresses
addresses_list = list(coordinates.keys())
for i in range(len(addresses_list) - 1):
    coord_1 = coordinates[addresses_list[i]]
    coord_2 = coordinates[addresses_list[i + 1]]
    # Calculate midpoint between two coordinates for label placement
    midpoint = [(coord_1[0] + coord_2[0]) / 2, (coord_1[1] + coord_2[1]) / 2]
    folium.PolyLine(
        locations=[coord_1, coord_2],
        color="blue",
        popup=f"Edge {i+1}",
        tooltip=f"Edge {i+1}",
    ).add_to(mymap)
    folium.Marker(
        location=midpoint,
        icon=folium.DivIcon(html=f'<div style="font-size: 10pt;">{i+1}</div>')
    ).add_to(mymap)

# Save the map to an HTML file
mymap.save("map_with_numbered_edges.html")