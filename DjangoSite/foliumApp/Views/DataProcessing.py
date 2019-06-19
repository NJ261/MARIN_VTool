from foliumApp.models import WorldBorder, Communities, MarineTrafficData, AllPorts

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
        communitiesList = Communities.objects.values_list('name', 'geom')
        processedData = []

        for i in range(0, len(communitiesList)):
            tempDict = json.loads(communitiesList[i][1].json)
            processedData.append([communitiesList[i][0], tempDict['coordinates']])

        # TODO: create a function here
        # swap lat, lng in a list to match the format
        for i in range(0, len(processedData)):
            processedData[i][1][0], processedData[i][1][1] = processedData[i][1][1], processedData[i][1][0]

        return processedData

    def getMarineTrafficData(self):
        marineTrafficData = MarineTrafficData.objects.values_list()
        dataList = []

        for i in range(0, len(marineTrafficData)):
            a = json.loads(marineTrafficData[i][1].json)
            a = a['coordinates']
            a = a[0]
            for i in range(0, len(a)):
                a[i][0], a[i][1] = a[i][1], a[i][0]

            dataList.append(a)
        return dataList

    def getAllPortsData(self):
        allPortsData = AllPorts.objects.values_list()
        return allPortsData

    def calculateGrids(self):
        import shapely.geometry
        import pyproj

        # Set up projections
        p_ll = pyproj.Proj(init='epsg:4326')
        p_mt = pyproj.Proj(init='epsg:3857') # metric; same as EPSG:900913

        # Create corners of rectangle to be transformed to a grid
        nw = shapely.geometry.Point((-70.0, 40.0))
        se = shapely.geometry.Point((-50.0, 60.0))

        stepsize = 500000 # 500 km grid step size

        # Project corners to target projection
        s = pyproj.transform(p_ll, p_mt, nw.x, nw.y) # Transform NW point to 3857
        e = pyproj.transform(p_ll, p_mt, se.x, se.y) # .. same for SE

        # Iterate over 2D area
        gridpoints = []
        x = s[0]
        while x < e[0]:
            y = s[1]
            while y < e[1]:
                p = shapely.geometry.Point(pyproj.transform(p_mt, p_ll, x, y))
                gridpoints.append(p)
                y += stepsize
            x += stepsize

        return gridpoints
