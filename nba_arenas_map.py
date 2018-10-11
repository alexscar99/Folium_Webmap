# Folium combines Python's strength of data handling with the mapping abilities
# of the leaflet.js library. Use Python code to manipulate data, and then
# visualize it in the browser as Leaflet compiles it to HTML, CSS, and JS.
import folium
import pandas

# Create DataFrame object from txt file and create lists for each column
data = pandas.read_csv('nba-arenas.txt')
latitude = list(data['LAT'])
longitude = list(data['LON'])
team = list(data['TEAM'])
arena = list(data['ARENA'])
capacity = list(data['CAPACITY'])
year_opened = list(data['OPENED'])
division = list(data['DIVISION'])

# Create list of lists to pass as *args later on during iteration
arena_info = [
    latitude, longitude, team, arena, capacity, year_opened, division
]


# Color code the markers based off of the division the NBA team plays in
def color_producer(division):
    return {
        'Atlantic': 'red',
        'Central': 'green',
        'Southeast': 'beige',
        'Pacific': 'orange',
        'Southwest': 'lightgray',
        'Northwest': 'purple'
    }[division]


# Iframe for when marker is selected
iframe_html = """
<div style="text-align: center">
<h3 style="color: #4D9078">%s</h3>
<h4 style="color: #f78154">%s</h4>
<h5 style="color: #666">Max Capacity of %s</h5>
<h5 style="color: #666">Opened in %s</h5>
</div>
"""

# NBA Arenas by Division legend
arena_legend_html = """
<div style="position: fixed; bottom: 20px; right: 15px; width: 220px;
height: 270px; border:2px solid; z-index:9999; font-size:14px;
">
    <p style="text-align: center; margin-top: 5px; font-weight: bold">
    NBA Arenas by Division</p> &nbsp;
    Atlantic &nbsp; <i class="fa fa-map-marker fa-lg" style="color:red">
    </i><br><br>
    &nbsp; 
    Central &nbsp; <i class="fa fa-map-marker fa-lg" style="color:green">
    </i><br><br>
    &nbsp;
    Southeast &nbsp; <i class="fa fa-map-marker fa-lg" style="color:#ffd78e">
    </i><br><br>
    &nbsp; 
    Pacific &nbsp; <i class="fa fa-map-marker fa-lg" style="color:orange">
    </i><br><br>
    &nbsp; 
    Southwest: &nbsp; <i class="fa fa-map-marker fa-lg" style="color: #999">
    </i><br><br>
    &nbsp; 
    Northwest &nbsp; <i class="fa fa-map-marker fa-lg" style="color:purple"></i>
</div>
"""

# Population by State legend
population_legend_html = """
<div style="position: fixed; bottom: 15px; left: 15px; width: 175px;
height: 190px; border:2px solid; z-index:9999; font-size:15px;
">
    <p style="text-align: center; margin-top: 10px; font-weight: bold">
    States by Population</p> &nbsp;
    10 million+ &nbsp; <i class="fa fa-area-chart fa-2x" style="color:#f29393">
    </i><br><br>&nbsp; 
    5-10 million &nbsp; <i class="fa fa-area-chart fa-2x" style="color: #a0d8a0">
    </i><br><br>
    &nbsp;
    5 million or less &nbsp; <i class="fa fa-area-chart fa-2x" 
    style="color:#ffd78e"></i><br><br>
    &nbsp; 
</div>
"""

# Generate Map object with initial location as list of latitude and longitude
# coordinates, an initial zoom level, min zoom level, and built-in tileset.
map = folium.Map(
    location=[38.58, -96.09], zoom_start=5, min_zoom=5, tiles='Mapbox Bright')

# Create Feature Group for NBA Arenas
fg_arenas = folium.FeatureGroup(name="NBA Arenas")

# Iterate through text file and add marker at location and create an iframe with
# all info regarding that arena. Add the iframe as a child of the feature group.
for lat, lon, team, arena, year, capacity, division in zip(*arena_info):
    iframe = folium.IFrame(
        html=iframe_html % (arena, team, str(year), str(capacity)),
        width=235,
        height=145)
    fg_arenas.add_child(
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(iframe),
            icon=folium.Icon(color_producer(division))))

# Add another feature group to color the map by population
fg_population = folium.FeatureGroup(name="Population")

# Open the JSON file with info on all 50 states, use lambda to add a different
# fillColor depending on population of that state. Add all of this as a child
# to the feature group.
fg_population.add_child(
    folium.GeoJson(open('states.json', encoding='utf-8-sig').read(),
                   style_function=lambda x: {'fillColor': '#96f296'
                   if x['properties']['population'] < 5000000 else 'orange'
                   if 5000000 <= x['properties']['population'] < 10000000
                   else '#eb5757'}))

# Add the feature groups to the Map object as child elements
map.add_child(fg_arenas)
map.add_child(fg_population)

# LayerControl gives option to toggle all layers except the base layer
map.add_child(folium.LayerControl())

# Add both legends (arena and population) to the Map object as children
map.get_root().html.add_child(folium.Element(arena_legend_html))
map.get_root().html.add_child(folium.Element(population_legend_html))

map.save('nba-arenas-map.html')