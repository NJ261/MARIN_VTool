from django.shortcuts import render, render_to_response
from geojson import Polygon
import folium

from foliumApp.Views.DataProjection import DataProjection
from foliumApp.Views.DataProcessing import DataProcessing

def index(request):
    lat, lon = DataProcessing().getLocation()
    map = folium.Map(location=[lat, lon], zoom_start=6)
    folium.Marker([lat, lon], tooltip='You are here: {}, {}'.format(lat, lon), icon=folium.Icon(color='green')).add_to(map)

    # canadaData = DataProcessing().geoJsonLayer('Canada')
    # map = DataProjection(color='black', fillColor='#ffff00').addGeoJsonLayer(map, canadaData, 'Canada')

    # plotting communities data
    communitiesData = DataProcessing().communitiesData()
    map = DataProjection().drawCommunitiesMarker(map, communitiesData)

    marineTrafficData = DataProcessing().getMarineTrafficData()
    map = DataProjection(weight=2, color='black').drawPolyLine(map, marineTrafficData, 'traffic')

    # sample grids
    # gridsData = DataProcessing().calculateGrids()
    # map = DataProjection().drawPoints(map, gridsData)

    folium.LayerControl().add_to(map)
    map.save('foliumApp/static/index.html')
    return render_to_response("index.html")
