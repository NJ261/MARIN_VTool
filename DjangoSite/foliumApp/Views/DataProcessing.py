from foliumApp.models import Communities, MarineTrafficData, Grids, Results

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

    def swapLatLngInList(self, data, loopNumbers):
        if loopNumbers >= 2:
            for i in range(0, len(data)):
                self.swapLatLngInList(data[i], loopNumbers - 1)
                data[i][0], data[i][1] = data[i][1], data[i][0]
        return data

    def getTimeDuration(self, vesselID):
        data = []
        result = Results.objects.filter(vesselid=vesselID)
        for i in range(0, len(result)):
            data.append(result[i].time)
        return data

    def getLocationData(self, vesselID, locationIndex):
        data = []
        result = Results.objects.filter(vesselid=vesselID)
        for i in range(0, locationIndex):
            data.append([float(result[i].lat), float(result[i].lng)])
        return data

    def getRemoteIndexColor(self, vesselID, locationIndex):
        result = Results.objects.filter(vesselid=vesselID)
        remoteIndex = int(result[locationIndex - 1].remoteindex)
        if remoteIndex == 1:
            color = 'darkgreen'
        elif remoteIndex == 2:
            color = 'lightred'
        else:
            color = 'red'
        return color

    def getVesselNamesList(self):
        vesselNamesList = []
        result = Results.objects.order_by().values('vesselid').distinct()
        for i in range(0, len(result)):
            vesselNamesList.append(result[i]['vesselid'])
        return vesselNamesList