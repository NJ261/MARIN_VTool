from django.shortcuts import render
from django.http import HttpResponse
from geojson import Polygon
import folium

from foliumApp.Views.DataProjection import DataProjection
from foliumApp.Views.DataProcessing import DataProcessing

def index(request):
    lat, lon = DataProcessing().getLocation()
    map = folium.Map(location=[lat, lon], zoom_start=6)
    folium.Marker([lat, lon], tooltip='You are here: {}, {}'.format(lat, lon)).add_to(map)

    canadaData = DataProcessing().geoJsonLayer('Canada')
    map = DataProjection(color='black', fillColor='#ffff00').addGeoJsonLayer(map, canadaData, 'Canada - Layer')

    # plotting communities data
    communitiesData = DataProcessing().communitiesData()
    map = DataProjection().drawCommunitiesMarker(map, communitiesData)

    folium.LayerControl().add_to(map)
    return HttpResponse(map._repr_html_())
