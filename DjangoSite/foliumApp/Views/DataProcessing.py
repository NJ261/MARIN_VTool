from foliumApp.models import WorldBorder, Communities, MarineTrafficData, AllPorts, Grids

import geocoder, json

class DataProcessing:

    # TODO: Documentation
    def __init__(self):
        pass

    def getLocation(self):
        myLocation = geocoder.ip('me')
        return myLocation.lat, myLocation.lng

    def getCommunitiesData(self):
        communitiesList = Communities.objects.values_list('name', 'geom')
        processedData = []

        # TODO: modify code based on convertDataToJson function
        for i in range(0, len(communitiesList)):
            tempDict = json.loads(communitiesList[i][1].json)
            processedData.append([communitiesList[i][0], tempDict['coordinates']])

        # TODO: modify code based on swapLatLngInList function
        # swap lat, lng in a list to match the format
        for i in range(0, len(processedData)):
            processedData[i][1][0], processedData[i][1][1] = processedData[i][1][1], processedData[i][1][0]

        return processedData

    def getMarineTrafficData(self):
        marineTrafficData = MarineTrafficData.objects.values_list()
        processedData = self.convertDataToJson(marineTrafficData, -1, 2)
        return processedData

    def getAllPortsData(self):
        # TODO: process this data and display it on map
        allPortsData = AllPorts.objects.values_list()
        return allPortsData

    def getGridsData(self):
        gridsData = Grids.objects.values_list()
        processedData = self.convertDataToJson(gridsData, -1, 2)
        return processedData

    def convertDataToJson(self, inputData, dataIndex, loopNumbers):
        jsonData = []
        for item in range(0, len(inputData)):
            tempData = json.loads(inputData[item][dataIndex].json)
            tempData = tempData['coordinates']
            tempData = tempData[0]
            tempData = self.swapLatLngInList(tempData, loopNumbers)
            jsonData.append(tempData)
        return jsonData

    def geoJsonLayer(self, layerName):
        data = WorldBorder.objects.get(name=layerName)
        return data.geom.geojson

    def swapLatLngInList(self, data, loopNumbers):
        if loopNumbers >= 2:
            for i in range(0, len(data)):
                self.swapLatLngInList(data[i], loopNumbers - 1)
                data[i][0], data[i][1] = data[i][1], data[i][0]
        return data
