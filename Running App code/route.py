import pandas as pd
import numpy as np
import googlemaps
import polyline
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyBEYZuox2CwkJRgPdE0l6zNnVYKXMdqshg')

# Load the crime dataset into a Pandas dataframe
crime_data = pd.read_csv('Updated_Crimes.csv')

# Extract the latitude and longitude columns and the total crime column
crime_locs = crime_data[['Latitude', 'Longitude']]



total_crime = crime_data['Total Crime']

latitudes = crime_data['Latitude']
longitudes = crime_data['Longitude']


# murders = crime_data['Murder ']
# raps = crime_data['Rape']
# robbery = crime_data['Robbery']
# kidnapping = crime_data['Kidnapping']
# harassment = crime_data['Harassment']

mask = []

def crime_list(route_points, crime_data):
    crimes_tags_list = []
    all_crime_numbers = []
    all_locations = []
    for p in route_points:
        row_mask = (np.isclose(crime_data['Latitude'], p[0], rtol=1e-3)) & (np.isclose(crime_data['Longitude'], p[1], rtol=1e-3))                           
        total_crime_number = total_crime[(np.isclose(crime_locs['Latitude'], p[0], rtol=1e-3)) & 
                          (np.isclose(crime_locs['Longitude'], p[1], rtol=1e-3))].sum()         
        # if True in row_mask:
        #     print ("YES: ", total_crime_number)        
        if True in row_mask and total_crime_number>0 and total_crime_number not in all_crime_numbers:
            all_crime_numbers.append(total_crime_number)
            #print("HERE")
            lati = crime_data['Latitude'][row_mask].values[0]
            longi = crime_data['Longitude'][row_mask].values[0]
            if (lati, longi) in all_locations:
                continue
            all_locations.append(  (lati, longi) )
            crimes_tags = {
                'Murder' : crime_data['Murder '][row_mask].values[0],
                'Raps' : crime_data['Rape'][row_mask].values[0],
                'Robbery' : crime_data['Robbery'][row_mask].values[0],
                'Kidnapping' : crime_data['Kidnapping'][row_mask].values[0],
                'Harassment' : crime_data['Harassment'][row_mask].values[0],
                'Latitude' : lati,
                'Longitude' : longi
            }       
            all_zeroes = False
            for k, v in crimes_tags.items():
                if k.lower() in ['latitude', 'longitude']:
                    continue
                if v !=0:
                    all_zeroes=True
            if all_zeroes:          
                crimes_tags_list.append(crimes_tags)
        crime_data = crime_data.drop(crime_data[row_mask].index)        
    print("tags count:", len(crimes_tags_list))
    return crimes_tags_list, crime_data


def sum_crime_for_route(route_points):
    # Calculate the sum of total crimes for each point in the route that exists in the dataset
    crimes = [total_crime[(np.isclose(crime_locs['Latitude'], p[0], rtol=1e-3)) & 
                          (np.isclose(crime_locs['Longitude'], p[1], rtol=1e-3))].sum()
             for p in route_points]
    return sum(crimes)

def crime_probability(sum_crime):
    # Calculate the probability of crime occurrence based on the crime statistics in the dataset
    total_crime_sum = total_crime.sum()
    prob = (sum_crime / total_crime_sum) if total_crime_sum > 0 else 0
    return prob

def get_top_routes(start_loc, end_loc):
    # Get directions between start and end locations
    directions_result = gmaps.directions(start_loc, end_loc, mode="driving", departure_time=datetime.now(), alternatives=True)  # Request multiple routes

    dynamic_crime_data = pd.read_csv('Updated_Crimes.csv')

    routes = []
    for route in directions_result:
        duration = route['legs'][0]['duration']['value']
        route_points = []
        steps = []
        for step in route['legs'][0]['steps']:
            steps.append(step)
            encoded_polyline = step['polyline']['points']
            decoded_polyline = polyline.decode(encoded_polyline)
            route_points.extend(decoded_polyline)
        sum_crime = sum_crime_for_route(route_points)
        crimes_tags_list, dynamic_crime_data = crime_list(route_points, dynamic_crime_data)       
        prob = crime_probability(sum_crime)
        routes.append({'steps': steps, 'duration': duration, 'points': route_points, 'probability': prob, 'tags': crimes_tags_list})

    # Return the top three routes based on crime probability
    # sorting largest to smallest
    sorted_routes = sorted(routes, key=lambda r: r['probability'], reverse=True)
    top_routes = sorted_routes[:3]
    top_routes.append(sorted_routes[-1])
    # Extract the route points for each of the top routes
    top_route_points = []
    top_steps = []
    for route in top_routes:
        top_route_points.append(route['points'])
        top_steps.append(route['steps'])
    
    # Return the top three routes along with the route points, duration, and probability
    return [
        {'steps': top_steps,'route_points': points, 'duration': route['duration'], 'probability': route['probability'], 'tags': route['tags']}         
            for points, route in zip(top_route_points, top_routes)] 



# for i, route in enumerate(top_routes):
#     print(f"Route {i+1}: {route['route_points']}, duration={route['duration']}s, probability={route['probability']}")

# start_loc = 'FREEDOM SQUARE PLAYGROUND, NY'
# end_loc = 'BLEECKER PLAYGROUND, NY'
# crimes_rates = get_top_routes(start_loc, end_loc)