from foliumApp.models import Communities, MarineTrafficData, Grids, Results, UniqueMMSI

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

    def getTimeDuration(self, sourcemmsi):
        data = []
        result = Results.objects.filter(sourcemmsi=sourcemmsi)
        uniqueDates = result.values('sourcedate').distinct().order_by('sourcedate')
        for i in range(0, len(uniqueDates)):
            uniqueTimeValues = result.filter(sourcedate=uniqueDates[i]['sourcedate']).values('sourcetime').distinct().order_by('sourcetime')
            for j in range(0, len(uniqueTimeValues)):
                data.append(uniqueDates[i]['sourcedate'] + ' ' + uniqueTimeValues[j]['sourcetime'])
        return data

    def getTrafficData(self, sourcemmsi, locationIndex):
        communities, vesselTraffic = [], []
        dateTime = locationIndex.split()
        result = Results.objects.filter(sourcemmsi=sourcemmsi).filter(sourcedate=dateTime[0]).filter(sourcetime=dateTime[1])
        for i in range(0, len(result)):
            targetName = result[i].targetmmsi.replace(" ", "") # removing space to check whether it is community
            if (targetName.isalpha() == True):
                communities.append([result[i].targetmmsi,[float(result[i].targetlng), float(result[i].targetlat)]])
            else:
                vesselTraffic.append([result[i].targetmmsi,[float(result[i].targetlng), float(result[i].targetlat)]])
        return communities, vesselTraffic

    def getLocationData(self, sourcemmsi, dateTimeData):
        locationData = []
        for i in range(0, len(dateTimeData)):
            dateTime = dateTimeData[i].split()
            result = Results.objects.filter(sourcemmsi=sourcemmsi).filter(sourcedate=dateTime[0]).filter(sourcetime=dateTime[1]).first()
            locationData.append([result.sourcelng, result.sourcelat])
        return locationData

    def getRemoteIndexColor(self, sourcemmsi, currentDateTime):
        dateTime = currentDateTime.split()
        result = Results.objects.filter(sourcemmsi=sourcemmsi).filter(sourcedate=dateTime[0]).filter(sourcetime=dateTime[1])
        minDistance = result.filter(minimum=True).values('distance').distinct().first()
        minDistance = float(minDistance['distance']) / 1000 #dividing distance by 1000 km
        if minDistance <= 1:
            color = 'darkgreen'
        elif minDistance >= 2:
            color = 'lightred'
        else:
            color = 'red'

        targetmmsi = result.filter(minimum=True).values('targetmmsi').distinct().first()
        targetmmsi = targetmmsi['targetmmsi']
        return color, targetmmsi, minDistance * 1000

    def getVesselNamesList(self):
        vesselNamesList = []
        result = UniqueMMSI.objects.order_by().values('sourcemmsi').distinct()
        for i in range(0, len(result)):
            vesselNamesList.append(result[i]['sourcemmsi'])
        return vesselNamesList