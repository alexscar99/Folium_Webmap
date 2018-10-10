# folium combines Python's strength of data handling with the mapping abilities
# of the leaflet.js library.
# Write Python code to manipulate data, then visualize it with a Leaflet map as
# leaflet.js translates it to HTML, CSS, and JS for the browser.
import folium
import pandas

# Create DataFrame object from txt file and create lists for lat and lon
data = pandas.read_csv('nba-arenas.txt')
latitude = list(data['LAT'])
longitude = list(data['LON'])

# Folium.Map --> generates a base `Map` object that can be passed
# many different parameters
# In this case, passing location as list of initial latitude
# and longitude coordinates, an initial zoom level, and
# a built-in tileset (Mapbox Bright).
map = folium.Map(location=[38.58, -96.09], zoom_start=5, tiles='Mapbox Bright')

# Feature Group allows you to add multiple features
fg = folium.FeatureGroup(name="NBA Arenas Map")

# Between Map object and save method you can add elements to the Feature Group
# Loop through text file and add marker at location
for lat, lon in zip(latitude, longitude):
    fg.add_child(
        folium.Marker(
            location=[lat, lon],
            popup='Hi I am a marker',
            icon=folium.Icon('green')))

# Add the feature group to the map as a child element
map.add_child(fg)

map.save('nba-arenas-map.html')