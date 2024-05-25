import folium

def find_center(route:list[tuple[int]]) -> tuple[int]:
    # Calculate the center of the route
    latitudes = [coord[0] for coord in route]
    longitudes = [coord[1] for coord in route]
    center = (sum(latitudes) / len(route), sum(longitudes) / len(route))
    return center

def render_map(route:list[tuple[int]], outfile:str):
    map_center = find_center(route)  # Centered on one of the coordinates
    mymap = folium.Map(location=map_center, zoom_start=13)

    for address, coord in route:
        folium.Marker(
            location=coord,
            popup=address,
        ).add_to(mymap)

    # Add edges between consecutive addresses
    for i, coord_1 in enumerate(route[:-1]):
        coord_2 = route[i + 1]
        # Calculate midpoint between two coordinates for label placement
        midpoint = [(coord_1[0] + coord_2[0]) / 2, (coord_1[1] + coord_2[1]) / 2]
        folium.PolyLine(
            locations=[coord_1, coord_2],
            color="blue",
            popup=f'<a href="https//:google.de" target="_blank">  {i+1}',
            tooltip=f"Edge {i+1}",
            
        ).add_to(mymap)
        folium.Marker(
            location=midpoint,
            icon=folium.DivIcon(html=f'<div style="font-size: 10pt;">{i+1}</div>')
        ).add_to(mymap)

    # Save the map to an HTML file
    mymap.save("map_with_numbered_edges.html")