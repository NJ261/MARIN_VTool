from foliumApp.models import WorldBorder, Communities

import geocoder, json

class DataProcessing:

    # TODO: Documentation
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

        # TODO: create a function here
        # swap lat, lng in a list to match the format
        for i in range(0, len(newDataList)):
            for j in range(0, len(newDataList[i])):
                newDataList[i][j][0], newDataList[i][j][1] = newDataList[i][j][1], newDataList[i][j][0]

        return newDataList

    def getLocation(self):
        myLocation = geocoder.ip('me')
        return myLocation.lat, myLocation.lng

    def communitiesData(self):
        communitiesList = Communities.objects.values_list('name', 'wkb_geometry')
        processedData = []

        for i in range(0, len(communitiesList)):
            tempDict = json.loads(communitiesList[i][1].json)
            processedData.append([communitiesList[i][0], tempDict['coordinates']])

        # TODO: create a function here
        # swap lat, lng in a list to match the format
        for i in range(0, len(processedData)):
            processedData[i][1][0], processedData[i][1][1] = processedData[i][1][1], processedData[i][1][0]

        return processedData
