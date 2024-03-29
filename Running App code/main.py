# -*- coding: utf-8 -*-
"""Main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1l1d0xejVcdJvYTnOeA0LhB-LgSwTK-SO

# Data Scraping
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# Define the URL to scrape the news headlines
url = 'https://news.google.com/search?q=new+york+city+crime&hl=en-US&gl=US&ceid=US%3Aen'

# Send a request to get the HTML content
res = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(res.content, 'html.parser')

# Find all the headlines and their dates
headlines = soup.find_all('div', class_='NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc')

# Create an empty dataframe to store the data
columns = ['Date', 'Headline']
crime_df = pd.DataFrame(columns=columns)

# Iterate over the headlines and extract the date and headline text
for headline in headlines:
    date = headline.find('time')['datetime']
    text = headline.find('a', class_='DY5T1d').text
    crime_df = crime_df.append({'Date': date, 'Headline': text}, ignore_index=True)

crime_df.head(5)

import pandas as pd
from nltk.stem import SnowballStemmer

# Create a stemmer object
stemmer = SnowballStemmer('english')

# Define the DataFrame and column to be stemmed
crime_df['Headline']

# Define a function to apply stemming to a single string
def stem_text(text):
    stemmed_words = [stemmer.stem(word) for word in text.split()]
    return ' '.join(stemmed_words)

# Apply the stemming function to the DataFrame
crime_df['Headline'] = crime_df['Headline'].apply(stem_text)

crime_df.head(5)

import pandas as pd
import matplotlib.pyplot as plt

# Load the news headlines
#news_df = pd.read_csv('crime_data.csv')

# Define the keywords to search for
keywords = ['crime', 'violent', 'accident']

# Initialize the count variables
total_headlines = len(crime_df)
keyword_headlines = 0

# Iterate through the headlines
for headline in crime_df['Headline']:
    # Check if the headline contains any of the keywords
    if any(keyword in headline.lower() for keyword in keywords):
        keyword_headlines += 1

# Print the results
print(f'Total headlines: {total_headlines}')
print(f'Headlines with keywords: {keyword_headlines}')
print(f'Headlines without keywords: {total_headlines - keyword_headlines}')

# Plot a histogram of the results
plt.hist([keyword_headlines, total_headlines - keyword_headlines])
plt.title('Headlines with and without Keywords')
plt.xlabel('Number of Headlines')
plt.ylabel('Frequency')
plt.legend(['With Keywords', 'Without Keywords'])
plt.show()

import pandas as pd

# Read the CSV file into a Pandas DataFrame
#df = pd.read_csv('crime_data.csv')

# Define a list of spcial characters to check for
special_chars = ['���', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=', '[', ']', '{', '}', '|', '\\', ';', ':', '\'', '\"', ',', '<', '>', '.', '/', '?']

# Create a function to check if a string contains any of the special characters
def has_special_chars(string):
    for char in special_chars:
        if char in string:
            return True
    return False

# Drop any rows where the statement in the specified column contains special characters between its words
df = crime_df[~crime_df['Headline'].apply(has_special_chars)]

crime_df.to_csv('crime_data.csv', index=False)

import spacy

# load the pre-trained NLP model
nlp = spacy.load('en_core_web_sm')

# define a function to extract locations from a statement
def extract_street_address(statement):
    # apply the NLP model to the statement
    doc = nlp(statement)
    
    # initialize empty lists to store city and street names
    cities = []
    streets = []
    
    # loop over each token in the document
    for token in doc:
        # if the token is a proper noun and its text is not "I"
        if token.pos_ == 'PROPN' and token.text != 'I':
            # if the token is labeled as a city in the NER output
            if token.ent_type_ == 'GPE':
                cities.append(token.text)
            # if the token is labeled as a street in the NER output
            elif token.ent_type_ == 'FAC':
                streets.append(token.text)
    
    # return the extracted city and street names as a dictionary
    #return {'cities': cities, 'streets': streets}
    return streets #

import re
import pandas as pd 
from geopy.geocoders import Nominatim
import datetime
import requests

###########################################################################################
data_set = pd.read_csv('Updated_Crimes.csv')
data_scrap = pd.read_csv('crime_data.csv')


# keywords
Murder_keywords = ["Murder", "Kill" , "Shot" ,"shot", "Homicide", "Manslaughter", "Assassination", "Killing", "Slaying", "Butchery", "Execution", 
            "Massacre", "Carnage", "Elimination", "Annihilation", "Taking a life", "Murderous act",
            "Death at the hands of another", "Violent death", "Cold-blooded killing", 
             "Fatal attack", "Premeditated murder", "Unlawful killing", "Culpable homicide",
             "First-degree murder", "Second-degree murder", "Felony murder"]

Kidnap_keywords = ["Robbery", "Burglary", "Theft", "Larceny", "Heist", "Mugging", "Hold-up", "Stick-up", "Raid", 
                   "Plunder", "Rip-off", "Stealing", "Snatching", "Embezzlement", "Pickpocketing", "Purse-snatching", "Armed robbery", 
                   "Bank robbery", "Carjacking", "Smash-and-grab robbery"]

rape_keywords = ["sexual assault", "rape" ,"sexual violence" ,"sexual abuse" ,"sexual misconduct" , "sexual harassment", "molestation"]

Harassment_Keywords = ["Harassment", "Intimidation", "Bullying", "Verbal abuse", "Sexual harassment", 
                       "Discrimination", "Stalking", "Cyberbullying", "Hate speech", "Threatening behavior", "Unwanted advances", 
                       "Catcalling", "Inappropriate behavior", "Coercion", "Blackmail", "Physical harassment", 
                       "Emotional abuse", "Psychological harassment", "Workplace harassment", "Racial harassment"]

Robbery_Snatching_Keywords = ["Snatch","robbe","Snatching" , "Grabbing", "Seizing", "Theft", "Robbery", "Larceny", "Purse-snatching", "Pickpocketing", "Theft by snatching",
                      "Street robbery", "Bag-snatching", "Chain-snatching", "Phone-snatching", "Mugging"]

#Loading the data into the dataframe
#df = pd.DataFrame(columns=columns)

# Example text
location_regex = r'on the\s*(\w+\s*)*|on\s*(\w+\s*)*,'
sentences = data_scrap['Headline']


# Extract the sentences that contain the keywords
#sentences = re.split('\. |\? |\! ', sentence)


for sentence in sentences:
    # Statement Checking Murder  
    for Murder_keyword in Murder_keywords:
      if any(re.search(r'\b{}\b'.format(Murder_keyword), sentence, re.IGNORECASE) for Murder_Keyword in Murder_keywords):  
          if re.search(location_regex, sentence, re.IGNORECASE):
              street_address = extract_street_address(sentence)   
              if street_address in data_set['Park '].values:
                  data_set.loc[data_set['Park '] == street_address, "Murder"] += 5  
              else:
                # Create a dictionary with column names and values
                new_row = {'Park ': street_address, 'Murder': 5, 'Robbery': 0, 'Rape': 0, 'Kidnapping': 0, 'Harassment': 0}
                # Append the dictionary as a new row to the dataset
                data_set = data_set.append(new_row, ignore_index=True) 
          else:
            break
      else:
         break 
       
            
    # Statement Checking Robbery 
    for Robbery_Snatching_Keyword in Robbery_Snatching_Keywords:
      if any(re.search(r'\b{}\b'.format(Robbery_Snatching_Keyword), sentence, re.IGNORECASE) for Robbery_Snatching_Keyword in Robbery_Snatching_Keywords):  
          if re.search(location_regex, sentence, re.IGNORECASE):
              street_address = extract_street_address(sentence)   
              if street_address in data_set['Park '].values:
                  data_set.loc[data_set['Park '] == street_address, "Robbery"] += 2  
              else:
                  # Create a dictionary with column names and values
                  new_row = {'Park ': street_address, 'Murder': 0, 'Robbery': 2, 'Rape': 0, 'Kidnapping': 0, 'Harassment': 0}
                  # Append the dictionary as a new row to the dataset
                  data_set = data_set.append(new_row, ignore_index=True) 
          else:
              break
      else:
          break 
        
    
    # Statement Checking Harassment
    for Harassment_Keyword in Harassment_Keywords:
        if any(re.search(r'\b{}\b'.format(Harassment_Keyword), sentence, re.IGNORECASE) for Harassment_Keyword in Harassment_Keywords):  
            if re.search(location_regex, sentence, re.IGNORECASE):
                street_address = extract_street_address(sentence)   
                if street_address in data_set['Park '].values:
                    data_set.loc[data_set['Park '] == street_address, "Harassment"] += 3  
                else:
                    # Create a dictionary with column names and values
                    new_row = {'Park ': street_address, 'Murder': 0, 'Robbery': 0, 'Rape': 0, 'Kidnapping': 0, 'Harassment': 3}
                    # Append the dictionary as a new row to the dataset
                    data_set = data_set.append(new_row, ignore_index=True) 
            else:
                break
        else:
            break 

  
#Statement Checking Rape  
  
    for rape_Keyword in rape_keywords:
        if any(re.search(r'\b{}\b'.format(rape_Keyword), sentence, re.IGNORECASE) for rape_keyword in rape_keywords):  
            if re.search(location_regex, sentence, re.IGNORECASE):
                street_address = extract_street_address(sentence)   
                if street_address in data_set['Park '].values:
                    data_set.loc[data_set['Park '] == street_address, "Rape"] += 4  
                else:
                    # Create a dictionary with column names and values
                    new_row = {'Park ': street_address, 'Murder': 0, 'Robbery': 0, 'Rape': 4, 'Kidnapping': 0, 'Harassment': 0}
                    # Append the dictionary as a new row to the dataset
                    data_set = data_set.append(new_row, ignore_index=True) 
            else:
                break
        else:
            break      


#Statement Checking Kidnapping 

    for rape_Keyword in rape_keywords:
        if any(re.search(r'\b{}\b'.format(Kidnap_keyword), sentence, re.IGNORECASE) for Kidnap_keyword in Kidnap_keywords):  
            if re.search(location_regex, sentence, re.IGNORECASE):
                street_address = extract_street_address(sentence)   
                if street_address in data_set['Park '].values:
                    data_set.loc[data_set['Park '] == street_address, "Rape"] += 3  
                else:
                    # Create a dictionary with column names and values
                    new_row = {'Park ': street_address, 'Murder': 0, 'Robbery': 0, 'Rape': 0, 'Kidnapping': 3, 'Harassment': 0}
                    # Append the dictionary as a new row to the dataset
                    data_set = data_set.append(new_row, ignore_index=True) 
            else:
                break
        else:
            break   






data_set.to_csv('Updated_Crimes.csv', index=False)

import pandas as pd
from geopy.geocoders import Nominatim
crime=pd.read_csv('updated_data.csv')
#print(crime.columns)
"""
crime['lat'] = ""
crime['long'] = ""
"""
geolocator = Nominatim(user_agent="myApp")

for i in crime.index:
    try:
        #tries fetch address from geopy
        location = geolocator.geocode(crime['Park '][i])
        
        #append lat/long to column using dataframe location
        crime.loc[i,'Latitude'] = location.latitude
        crime.loc[i,'Longitude'] = location.longitude
  
    except:
        #catches exception for the case where no value is returned
        #appends null value to column
        crime.loc[i,'Latitude'] = ""
        crime.loc[i,'Longitude'] = ""

print(crime.columns)
"""
location = geolocator.geocode(crime["Park"][10])
print(location.latitude, location.longitude)    
#40.74313843618834, -73.73852180697574
"""

import pandas as pd 
Crimes = pd.read_csv('Updated_Crimes.csv')
Crimes.head(5)

import locale
locale.getpreferredencoding = lambda: "UTF-8"

pip install GoogleMaps

pip install geopy

import pandas as pd
import re

crime_data = pd.read_csv('Updated_Crimes.csv')

missing_park = crime_data['Park '].isnull().sum()
print('Number of missing parks:', missing_park)

crime_data = crime_data.dropna(subset=['Park '])

import googlemaps
from datetime import datetime

def get_route_points(start_loc, end_loc):
    # Initialize Google Maps client
    gmaps = googlemaps.Client(key='AIzaSyBEYZuox2CwkJRgPdE0l6zNnVYKXMdqshg')

    # Get directions between start and end locations
    directions_result = gmaps.directions(start_loc, end_loc, mode="driving", departure_time=datetime.now())

    # Extract route points from directions
    route_points = []
    for step in directions_result[0]['legs'][0]['steps']:
        route_points.extend(step['polyline']['points'])

    return route_points

def get_crime_score(route_point, crime_data):
    # Find addresses in crime data that match the route point
    matching_addresses = crime_data[crime_data['Park '].str.contains(route_point)]
    
     # Escape special characters in route_point string
    route_point_escaped = re.escape(route_point)
    
    # Find addresses in crime data that match the route point
    matching_addresses = crime_data[crime_data['Park '].str.contains(route_point_escaped)]

    # Calculate total crime score for matching addresses
    crime_score = matching_addresses['Total Crime'].sum()

    return crime_score

import re

def get_crime_score(route_point, crime_data):
    # Escape special characters in route point string
    route_point_escaped = re.escape(route_point)
    
    # Find addresses in crime data that match the route point
    matching_addresses = crime_data[crime_data['Park '].str.contains(route_point_escaped)]

    # Calculate total crime score for matching addresses
    crime_score = matching_addresses['Total Crime'].sum()

    return crime_score

pip install polyline

import googlemaps
import polyline

gmaps = googlemaps.Client(key='AIzaSyBEYZuox2CwkJRgPdE0l6zNnVYKXMdqshg')

def get_route_points(start_loc, end_loc):
    # Get directions between start and end locations
    directions_result = gmaps.directions(start_loc, end_loc, mode="driving", departure_time=datetime.now())

    # Extract route points from directions
    route_points = []
    for step in directions_result[0]['legs'][0]['steps']:
        encoded_polyline = step['polyline']['points']
        decoded_polyline = polyline.decode(encoded_polyline)
        route_points.extend(decoded_polyline)

    return route_points

start_loc = 'FREEDOM SQUARE PLAYGROUND, NY'
end_loc = 'BLEECKER PLAYGROUND, NY'

route_points = get_route_points(start_loc, end_loc)

print(route_points)

pip install googlemaps

pip install polyline

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

def sum_crime_for_route(route_points):
    # Calculate the sum of total crimes for each point in the route that exists in the dataset
    crimes = [total_crime[(np.isclose(crime_locs['Latitude'], p[0])) & 
                          (np.isclose(crime_locs['Longitude'], p[1]))].sum() 
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

    routes = []

    for route in directions_result:
        duration = route['legs'][0]['duration']['value']
        route_points = []
        for step in route['legs'][0]['steps']:
            encoded_polyline = step['polyline']['points']
            decoded_polyline = polyline.decode(encoded_polyline)
            route_points.extend(decoded_polyline)
        sum_crime = sum_crime_for_route(route_points)
        prob = crime_probability(sum_crime)
        routes.append({'duration': duration, 'points': route_points, 'probability': prob})

    # Return the top three routes based on crime probability
    top_routes = sorted(routes, key=lambda r: r['probability'], reverse=True)[:3]
    
    # Extract the route points for each of the top routes
    top_route_points = []
    for route in top_routes:
        top_route_points.append(route['points'])
    
    # Return the top three routes along with the route points, duration, and probability
    return [{'route_points': points, 'duration': route['duration'], 'probability': route['probability']} 
            for points, route in zip(top_route_points, top_routes)]
 

start_loc = 'FREEDOM SQUARE PLAYGROUND, NY'
end_loc = 'BLEECKER PLAYGROUND, NY'

top_routes = get_top_routes(start_loc, end_loc)

for i, route in enumerate(top_routes):
    print(f"Route {i+1}: {route['route_points']}, duration={route['duration']}s, probability={route['probability']}")

import re
import pandas as pd

crime_data = pd.read_csv('Updated_Crimes.csv')

crime_data['lat_lon'] = crime_data.apply(lambda row: f"{row['Latitude']},{row['Longitude']}", axis=1)

def get_crime_score(route_point, crime_data):
    # Escape special characters in route point string
    route_point_escaped = re.escape(route_point)
    
    # Find addresses in crime data that match the route point
    matching_addresses = crime_data[crime_data['lat_lon'].str.contains(route_point_escaped)]

    # Calculate total crime score for matching addresses
    crime_score = matching_addresses['Total Crime'].sum()

    return crime_score

import folium
 
# Create a map centered on New York City
nyc_map = folium.Map(location=[40.730610, -73.935242], zoom_start=12)



# Add the route points to the map as a polyline
#route_points = [(40.748817, -73.985428), (40.726856, -73.996556), (40.728581, -73.985358)]
route_line = folium.PolyLine(locations=route_points, weight=3, color='Red')
nyc_map.add_child(route_line)

#print(crime_points)
# Display the map
nyc_map



