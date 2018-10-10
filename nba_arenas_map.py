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
team = list(data['TEAM'])
arena = list(data['ARENA'])
capacity = list(data['CAPACITY'])
year_opened = list(data['OPENED'])
division = list(data['DIVISION'])

arena_info = [
    latitude, longitude, team, arena, capacity, year_opened, division
]


def color_producer(division):
    return {
        'Atlantic': 'red',
        'Central': 'green',
        'Southeast': 'beige',
        'Pacific': 'orange',
        'Southwest': 'lightgray',
        'Northwest': 'purple'
    }[division]


html = """
<div style="text-align: center">
<h3 style="color: #4D9078">%s</h3>
<h4 style="color: #f78154">%s</h4>
<h5 style="color: #666">Max Capacity of %s</h5>
<h5 style="color: #666">Opened in %s</h5>
</div>
"""

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
for lat, lon, team, arena, year, capacity, division in zip(*arena_info):
    iframe = folium.IFrame(
        html=html % (arena, team, str(year), str(capacity)),
        width=235,
        height=145)
    fg.add_child(
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(iframe),
            icon=folium.Icon(color_producer(division))))

fg.add_child(folium.GeoJson(open('world.json', encoding='utf-8-sig').read()))

# Add the feature group to the map as a child element
map.add_child(fg)

map.save('nba-arenas-map.html')