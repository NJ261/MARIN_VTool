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


    onePolygon = Polygon([[[-61.199997, 45.558327],[-61.20472, 45.555267],[-61.212776, 45.556656],
                            [-61.219994, 45.55999],[-61.224167, 45.56415600000014],[-61.222221, 45.569443],
                            [-61.214165, 45.568886000000134],[-61.208611, 45.567215],[-61.202499, 45.563324],[-61.199997, 45.558327]]])
    map = DataProjection().addGeoJsonLayer(map, onePolygon, 'Blue Polygon')


    secondPolygon = Polygon([[[-61.199997, 45.558327],[-61.20472, 45.555267], [-61.212776, 45.556656],
                            [-61.219994, 45.55999],[-61.224167, 45.56415600000014],[-61.199997, 45.558327],
                            [-61.208611, 45.567215],[-61.202499, 45.563324]]])
    map = DataProjection(color='green', fillColor='green').addGeoJsonLayer(map, secondPolygon, 'Green Polygon')


    thirdPolygon = Polygon([[[-61.199997, 45.558327],[-61.20472, 45.555267],[-61.212776, 45.556656],
                            [-61.219994, 45.55999]]])
    map = DataProjection(color='red', fillColor='red').addGeoJsonLayer(map, thirdPolygon, 'Red Polygon')


    lineOne = [[44.636992, -63.587419],[44, -62],[43, -61], [43, -60]]
    map = DataProjection(color='red', opacity=0.8).drawPolyLine(map, lineOne, 'Line One')


    lineTwo = [[44.636992, -63.587419],[44, -61], [43, -59], [43, -57]]
    map = DataProjection().drawPolyLine(map, lineTwo, 'Line Two')

    folium.LayerControl().add_to(map)
    return HttpResponse(map._repr_html_())
