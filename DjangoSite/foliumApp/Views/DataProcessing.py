from foliumApp.models import WorldBorder

import geocoder

class DataProcessing:

    # ToDo: Documentation
    def __init__(self):
        pass

    def geoJsonLayer(self, layerName):
        data = WorldBorder.objects.get(name=layerName)
        return data.geom.geojson

    def swapLatLngInList(self, data):
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

    def getLocation(self):
        myLocation = geocoder.ip('me')
        return myLocation.lat, myLocation.lng
