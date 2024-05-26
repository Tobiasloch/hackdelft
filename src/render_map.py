import folium

def find_center(route:list[tuple[int]]) -> tuple[int]:
    # Calculate the center of the route
    latitudes = [coord[1][0] for coord in route]
    longitudes = [coord[1][1] for coord in route]
    center = (sum(latitudes) / len(route), sum(longitudes) / len(route))
    return center

def render_map(route:list[tuple[int]], outfile:str):
    map_center = find_center(route)  # Centered on one of the coordinates
    mymap = folium.Map(location=map_center, zoom_start=13)

    # Add markers for each address
    for address, coord in route:
        if address == 'Mekelweg 4, 2628 CD Delft':
            folium.Marker(
                location=coord,
                popup=address,
                icon=folium.Icon(color='orange', icon='fa-solid fa-house', prefix='fa')
            ).add_to(mymap)
        else:
            folium.Marker(
                location=coord,
                popup=address,
            ).add_to(mymap)

    # Add edges between consecutive addresses
    for i, (address, coord) in enumerate(route[:-1]):
        coord_1 = coord
        coord_2 = route[i + 1][1]
        
        # Draw the polyline
        folium.PolyLine(
            locations=[coord_1, coord_2],
            color="blue",
            weight=7,  # Adjust weight as needed
            opacity=0.7,
            tooltip=f"Edge {i+1}",
        ).add_to(mymap)

        # Calculate midpoint between two coordinates for label placement
        midpoint = [(coord_1[0] + coord_2[0]) / 2, (coord_1[1] + coord_2[1]) / 2]
        
        # Add a marker at the midpoint with a popup for the route
        folium.Marker(
            location=midpoint,
             icon=folium.DivIcon(
                #html='<div style="font-size: 24pt; color: red;"><i class="fa-solid fa-route"></i></div>',
                html='<div style="font-size: 24pt; color: red; transform: translate(-50%, -50%);"><i class="fa-solid fa-route"></i></div>',
                icon_size=(24, 24),
                #icon_anchor=(12, 12),
            ),
            popup=folium.Popup(f'Edge {i+1}<br><a href="https://www.google.com/maps/dir/?api=1&origin={coord_1[0]},{coord_1[1]}&destination={coord_2[0]},{coord_2[1]}&travelmode=driving" target="_blank">Route to next node</a>', max_width=300),
        ).add_to(mymap)

    # Save the map to an HTML file
    mymap.save(outfile)