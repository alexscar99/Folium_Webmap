# folium combines Python's strength of data handling with the mapping abilities
# of the leaflet.js library.
# Write Python code to manipulate data, then visualize it with a Leaflet map as
# leaflet.js translates it to HTML, CSS, and JS for the browser.
import folium

# Folium.Map --> generates a base `Map` object that can be passed
# many different parameters
# In this case, passing location as list of initial latitude
# and longitude coordinates, an initial zoom level, and
# a built-in tileset (Mapbox Bright).
map = folium.Map(
    location=[41.947521, -87.673645], zoom_start=6, tiles='Mapbox Bright')

map.save('map1.html')