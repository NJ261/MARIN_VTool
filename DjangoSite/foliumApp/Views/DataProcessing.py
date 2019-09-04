from foliumApp.models import Communities, Results, UniqueMMSI

import geocoder, json

class DataProcessing:

    # TODO: Documentation
    def __init__(self):
        pass

    # get IP based location
    def getLocation(self):
        myLocation = geocoder.ip('me')
        return myLocation.lat, myLocation.lng

    # get communities data for main page
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

    # Redundant - for reference
    def getMarineTrafficData(self):
        marineTrafficData = MarineTrafficData.objects.values_list()
        processedData = self.convertDataToJson(marineTrafficData, -1, 2)
        return processedData

    # Redundant - for reference
    def getGridsData(self):
        gridsData = Grids.objects.values_list()
        processedData = self.convertDataToJson(gridsData, -1, 2)
        return processedData

    # Redundant - for reference
    def convertDataToJson(self, inputData, dataIndex, loopNumbers):
        jsonData = []
        for item in range(0, len(inputData)):
            tempData = json.loads(inputData[item][dataIndex].json)
            tempData = tempData['coordinates']
            tempData = tempData[0]
            tempData = self.swapLatLngInList(tempData, loopNumbers)
            jsonData.append(tempData)
        return jsonData

    # Redundant - for reference
    # Recursion for swapping lat, lng
    def swapLatLngInList(self, data, loopNumbers):
        if loopNumbers >= 2:
            for i in range(0, len(data)):
                self.swapLatLngInList(data[i], loopNumbers - 1)
                data[i][0], data[i][1] = data[i][1], data[i][0]
        return data

    # getting date, time values for a source mmsi
    def getTimeDuration(self, sourcemmsi):
        data = []
        result = Results.objects.filter(sourcemmsi=sourcemmsi)
        uniqueDates = result.values('sourcedate').distinct().order_by('sourcedate')
        for i in range(0, len(uniqueDates)):
            uniqueTimeValues = result.filter(sourcedate=uniqueDates[i]['sourcedate']).values('sourcetime').distinct().order_by('sourcetime')
            for j in range(0, len(uniqueTimeValues)):
                data.append(uniqueDates[i]['sourcedate'] + ' ' + uniqueTimeValues[j]['sourcetime'])
        return data

    # getting traffic data (communities, other vessels) for a given date, time
    def getTrafficData(self, sourcemmsi, locationIndex):
        communities, vesselTraffic = [], []
        dateTime = locationIndex.split()
        result = Results.objects.filter(sourcemmsi=sourcemmsi).filter(sourcedate=dateTime[0]).filter(sourcetime=dateTime[1])
        for i in range(0, len(result)):
            targetName = result[i].targetmmsi.replace(" ", "") # removing space to check whether it is community
            if (targetName.isalpha() == True):
                communities.append([result[i].targetmmsi,[float(result[i].targetlng), float(result[i].targetlat)]]) # fetching communities data
            else:
                vesselTraffic.append([result[i].targetmmsi,[float(result[i].targetlng), float(result[i].targetlat)]]) # fetching other vessels data
        return communities, vesselTraffic

    # getting location (lat, lng) data till current location for source mmsi
    def getLocationData(self, sourcemmsi, dateTimeData):
        locationData = []
        for i in range(0, len(dateTimeData)):
            dateTime = dateTimeData[i].split()
            result = Results.objects.filter(sourcemmsi=sourcemmsi).filter(sourcedate=dateTime[0]).filter(sourcetime=dateTime[1]).first()
            locationData.append([result.sourcelng, result.sourcelat])
        return locationData

    # get marker's color based on remoteness, min distance and target mmsi
    def getRemoteIndexColor(self, sourcemmsi, currentDateTime):
        dateTime = currentDateTime.split()
        result = Results.objects.filter(sourcemmsi=sourcemmsi).filter(sourcedate=dateTime[0]).filter(sourcetime=dateTime[1])

        # getting distance for a date and time where minimum flag is True
        minDistance = result.filter(minimum=True).values('distance').distinct().first()
        minDistance = float(minDistance['distance']) / 1000 # dividing distance by 1000 km

        # distance / 1000 km is less than 1 then remoteness color: red, if it is between 1 to 2 then lightred, otherwise it would be red
        if minDistance <= 1:
            color = 'darkgreen'
        elif minDistance >= 2:
            color = 'lightred'
        else:
            color = 'red'

        # getting target mmsi respected to minimum distance row
        targetmmsi = result.filter(minimum=True).values('targetmmsi').distinct().first()
        targetmmsi = targetmmsi['targetmmsi']
        return color, targetmmsi, minDistance * 1000

    # getting list of source mmsi for main page
    def getVesselNamesList(self):
        vesselNamesList = []
        result = UniqueMMSI.objects.order_by().values('sourcemmsi').distinct()
        for i in range(0, len(result)):
            vesselNamesList.append(result[i]['sourcemmsi'])
        return vesselNamesList