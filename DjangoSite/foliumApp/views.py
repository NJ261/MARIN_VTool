from django.shortcuts import render
from django.http import HttpResponse
from .models import WorldBorder
from geojson import Polygon
import geocoder, folium, json

from foliumApp.Views.DataProjection import DataProjection

def index(request):
    lat, lon = getLocation()
    map = folium.Map(location=[lat, lon], zoom_start=6)
    folium.Marker([lat, lon], tooltip='You are here: {}, {}'.format(lat, lon)).add_to(map)

    canadaData = oneGeoJsonLayer(['Canada'])
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

# ToDo: move rest of the processing functions to DataProceesing class
def oneGeoJsonLayer(name):
    tempList = []
    for i in range(0, len(name)):
        ind = WorldBorder.objects.get(name=name[i])
    return ind.geom.geojson

def jsonDataLayer(name):
    ind = WorldBorder.objects.get(name=name)
    tempList = []
    data = json.loads(ind.geom.json)
    dataList = data['coordinates']
    tempList.append(dataList)
    return tempList

def processedData(data):
    # remove extra list from data: list of list to list for easy mapping
    newDataList = []

    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            newDataList.append([item for sublist in data[i][j] for item in sublist])

    # swap lat, lng in a list to match the format
    for i in range(0, len(newDataList)):
        for j in range(0, len(newDataList[i])):
            newDataList[i][j][0], newDataList[i][j][1] = newDataList[i][j][1], newDataList[i][j][0]

    return newDataList

def getLocation():
    myLocation = geocoder.ip('me')
    return myLocation.lat, myLocation.lng
