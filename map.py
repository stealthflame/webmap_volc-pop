import folium
import pandas

data = pandas.read_csv("volcanoes.csv")

lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = data["NAME"]

def color_producer(elevation):
	if elevation < 1000:
		return "green"
	elif 1000 <= elevation <3000:
		return "orange"
	else:
		return "red"



map = folium.Map(location=[42.000180, 11.887328], zoom_start=2, tiles="Mapbox Bright")

fgv = folium.FeatureGroup(name = "Volcanoes")
fgp = folium.FeatureGroup(name = "Population")


fgp.add_child(folium.GeoJson(data=open("world.json", "r",encoding ="utf-8-sig").read(),
	style_function=lambda x: {"fillColor":"green" if x["properties"]["POP2005"] < 10000000
	 else "orange" if 10000000 <= x["properties"]["POP2005"] < 20000000 else "red"}))
for lt,ln,el,nm in zip(lat,lon,elev,name):
	fgv.add_child(folium.CircleMarker(location=[lt,ln], popup=folium.Popup(str(nm)+" "+ str(el) + " m.",
		parse_html=True), fill_color=color_producer(el),radius = 6,fill_opacity=0.7,color='black'))

map.add_child(fgp)
map.add_child(fgv)
map.add_child(folium.LayerControl())
map.save("Map.html")
