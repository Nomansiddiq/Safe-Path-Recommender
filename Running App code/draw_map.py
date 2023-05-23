from route import get_top_routes
import folium

def get_map(source, destination):

    # start_loc = 'FREEDOM SQUARE PLAYGROUND, NY'
    # end_loc = 'BLEECKER PLAYGROUND, NY'

    top_routes = get_top_routes(source, destination)

    #print("Answer:", len(top_routes))
    assert  len(top_routes) != 0

    
    # Create a map centered on New York City
    nyc_map = folium.Map(location=[40.730610, -73.935242], zoom_start=12)
    # Add the route points to the map as a polyline
    #route_points = [(40.748817, -73.985428), (40.726856, -73.996556), (40.728581, -73.985358)]

    #for i in range(0, 3):
    route_points = top_routes[0]['route_points']
    route_line = folium.PolyLine(locations=route_points, weight=2, color='Red',  dash_array='5, 5')
    nyc_map.add_child(route_line)

    route_points = top_routes[1]['route_points']
    route_line = folium.PolyLine(locations=route_points, weight=2, color='Blue', dash_array='10, 10')
    nyc_map.add_child(route_line)

    route_points = top_routes[2]['route_points']
    route_line = folium.PolyLine(locations=route_points, weight=2, color='Black', dash_array='20, 20')
    nyc_map.add_child(route_line)

    route_points = top_routes[-1]['route_points']
    from folium.plugins import PolyLineTextPath
    route_line = folium.PolyLine(locations=route_points, weight=3, color='Green', dash_array='5, 5', overlay=True)
    
    # Draw Instructions
    for step in top_routes[-1]['steps'][-1]:
        popup_html = f"""
            <div style="background-color: #fff;
                    border: 2px solid #000;
                    border-radius: 5px;
                    padding: 10px;
                    font-family: Arial, sans-serif;">
                    {step['html_instructions']}
            </div>
        """
        folium.Marker(
            location=(step['end_location']['lat'], step['end_location']['lng']),
            tooltip = popup_html,
            icon=folium.Icon(icon='info-sign')
        ).add_to(nyc_map)

    nyc_map.add_child(route_line)

    # Add markers
    start = route_points[0]
    end = route_points[-1]


    # create an icon object with number in center
    icon_number = 5
    icon_size = 50
    icon_color = 'red'
    from folium import plugins
    

    for route in top_routes:
        for tags in route['tags']:
            name = ""
            total_crimes = 0
            for k, v in tags.items():
                name += f"{k}:{v}\n"
                if k.lower() not in ['latitude', 'longitude']:
                    total_crimes += v            
            popup_html = f"""
                <div style="background-color: #fff;
                        border: 2px solid #000;
                        border-radius: 5px;
                        padding: 10px;
                        font-family: Arial, sans-serif;">
                        {name}
                </div>
            """
            icon = folium.Icon(icon='people-robbery', prefix='fa', color=icon_color)
            folium.Marker(
                location= (tags['Latitude'], tags['Longitude']),
                popup=name,
                icon=icon,
                tooltip=popup_html
            ).add_to(nyc_map)
    # for point, name in zip([start, end], ["START", "END"]):
    #     folium.Marker(
    #         location= point ,
    #         popup=name,
    #     ).add_to(nyc_map)

    ### START
    icon = folium.Icon(icon='route', prefix='fa', color="green")            
    folium.Marker(
        location= start ,
        popup="Start",
        icon = icon,
        tooltip="Start"
    ).add_to(nyc_map)
    ### END
    icon = folium.Icon(icon='route', prefix='fa', color="green")            
    folium.Marker(
        location= end ,
        popup="End",
        icon = icon,
        tooltip="End"
    ).add_to(nyc_map)


    #print(crime_points)
    # Display the map
    
    folium.TileLayer('OpenStreetMap').add_to(nyc_map)
    folium.TileLayer('Stamen Terrain').add_to(nyc_map)
    folium.TileLayer('Stamen Toner').add_to(nyc_map)
    folium.TileLayer('Stamen Water Color').add_to(nyc_map)
    folium.TileLayer('cartodbpositron').add_to(nyc_map)
    folium.TileLayer('cartodbdark_matter').add_to(nyc_map)
    folium.LayerControl().add_to(nyc_map)

    nyc_map.save("./templates/routes.html")
    pass