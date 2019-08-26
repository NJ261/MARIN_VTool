#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 8/15/19 2:23 AM

@author: nirav
"""
import sys
sys.path.insert(0, '../Algorithms/')

from functools import partial
from shapely.ops import transform
from shapely import wkb
from shapely.geometry import Point
import pandas as pd
import pyproj

import CSVtoMatrix, Graph, Djikstra

class NWPDataProcessing:
    '''
    Description:
    ------------
    Perform following operations on NWP data: processing, mapping of grids to nwp data, distance calculations

    Parameters:
    -----------
    **kwargs :
             gridsCol : set grid's data geometry column by default it is 'geom'.
             landAreaCol : set land's data geometry column by default it is 'geom'.
             sourceCRS : set source projection to change CRS by default it is 'epsg:3978'.
             destCRS : set destination projection to change CRS by default it is 'epsg:4269'.
    '''

    def __init__(self, **kwargs):
        self.gridsTargetCol = kwargs.get('gridsCol', 'geom')
        self.landAreaTargetCol = kwargs.get('landAreaCol','geom')
        self.sourceCRS = kwargs.get('sourceCRS', 'epsg:3978')
        self.destinationCRS = kwargs.get('destCRS', 'epsg:4269')
        self.geod = pyproj.Geod(ellps='WGS84')
        self.project = partial(pyproj.transform,
                               pyproj.Proj(init=self.sourceCRS), #source co-ordinate system
                               pyproj.Proj(init=self.destinationCRS)) # destination co-ordinate system


    # filter nwpData: take only values which have more than 6 hrs total duration, reject the rest.
    def filterData(self, inputData):
        processedData = []
        uniqueMMSI = list(set(inputData['mmsi']))

        for i in range(0, len(uniqueMMSI)):
            df = inputData.loc[inputData['mmsi'] == uniqueMMSI[i]]  # find all values in dataframe for each mmsi, result will be a new dataframe
            sumElpSec = 0

            # here taking a row at 6 hour interval (21600 secs) with elp sec
            if sum(df['elp_sec']) > 21600:

                # inserting first value as second counter (i.e sumSecs) would be at zero
                processedData.append(df.loc[df.index[0]].values.tolist())
                for i in df.index:
                    sumElpSec = sumElpSec + df['elp_sec'][i]
                    if sumElpSec > 21600:
                        # inserting values at 6 hour duration and resetting counter
                        # here, travel routes with less than 6 hr duration will be rejected
                        processedData.append(df.loc[i].values.tolist())
                        sumElpSec = 0

                # inserting last value i.e destination
                processedData.append(df.loc[df.index[-1]].values.tolist())

        # converting processed list into dataframe and return it with unique MMSI list to the user
        processedData = pd.DataFrame(processedData, columns=['mmsi', 'elp_sec', 'st_date', 'geom'])
        return processedData, uniqueMMSI

    # convert data from wkb hex format to separate lat, lng
    def convertLatLng(self, processedData):
        processedData['lat'] = ''
        processedData['lng'] = ''

        for i in range(0, len(processedData)):
            lineString = wkb.loads(processedData['geom'][i], hex=True)  # reading wkb hex format data
            cnvrtedLineString = transform(self.project, lineString)  # tranforming data here
            processedData.loc[processedData.index[i], 'lat'] = cnvrtedLineString.convex_hull.xy[0][0]  # lat
            processedData.loc[processedData.index[i], 'lng'] = cnvrtedLineString.convex_hull.xy[1][0]  # lng
        del processedData['geom']
        return processedData

    # split 'st_date' column into 2 separate date and time columns
    def splitDateTime(self, processedData):
        processedData['date'] = ''
        processedData['time'] = ''
        for i in range(0, len(processedData)):
            tempString = processedData['st_date'][i].split()
            processedData.loc[processedData.index[i], 'date'] = tempString[0]
            processedData.loc[processedData.index[i], 'time'] = tempString[1]
        del processedData['st_date']
        return processedData


    # for each MMSI it finds other MMSI on a given date and time
    # Here, for time: finding values aganist +/- 3 hours duration from a given time (hence, 6 hr total interval) within 2500 km radius
    def sortValuesByDateTime(self, filteredData, uniqueMMSI, communityData):
        processedData = []
        for i in range(0, len(uniqueMMSI)):
            df = filteredData.loc[filteredData['mmsi'] == uniqueMMSI[i]]  ## find all values in dataframe for each mmsi, result will be a new dataframe
            for j in df.index:
                dateStr = df['date'][j]  # date - yyyy-mm-dd
                timeStr = df['time'][j]  # time - hr:min:sec
                hour = int(timeStr[:2])  # hour

                # select * from dateDF where date is %
                dateDF = filteredData.loc[filteredData['date'] == dateStr]
                for k in dateDF.index:

                    # avoiding same row against same mmsi
                    if df['mmsi'][j] != dateDF['mmsi'][k]:

                        # checking hour in 6 hrs duration (+/- 3 hrs each side)
                        if hour - 3 < int(dateDF['time'][k][:2]) < hour + 3:

                            # radius to search mmsi (vessel to vessel) is 2500 km
                            distance = self.geod.inv(df['lng'][j], df['lat'][j], dateDF['lng'][k], dateDF['lat'][k])
                            if (distance[-1] / 1000) <= 2500:
                                # storing values in following format: sourceMMSI, targetMMSI, sourceDate, sourceTime, targetDate, targetTime, sourceLat, sourceLng, targetLat, targetLng
                                processedData.append([df['mmsi'][j], dateDF['mmsi'][k],
                                                      df['date'][j], df['time'][j],
                                                      dateDF['date'][k], dateDF['time'][k],
                                                      df['lat'][j], df['lng'][j],
                                                      dateDF['lat'][k], dateDF['lng'][k]])
                
                # adding communities which are in radius (2500 km)
                for l in communityData.index:
                    community = wkb.loads(communityData['geom'][l], hex=True)
                    # radius to search mmsi (vessel to Communities) is 2500 km
                    distance = self.geod.inv(df['lat'][j], df['lng'][j], community.x, community.y)
                    if (distance[-1] / 1000) <= 2500:
                        # storing values in following format: sourceMMSI, targetMMSI (community name), sourceDate, sourceTime,
                                                            # targetDate (empty), targetTime (empty), sourceLat, sourceLng, targetLat, targetLng
                        processedData.append([df['mmsi'][j], communityData['name'][l],
                                              df['date'][j], df['time'][j],
                                              'NA', 'NA',
                                              df['lat'][j], df['lng'][j],
                                              community.x, community.y])
                    
        processedData = pd.DataFrame(processedData,
                                     columns=['sourceMMSI', 'targetMMSI', 'sourceDate', 'sourceTime', 'targetDate',
                                              'targetTime', 'sourceLat', 'sourceLng', 'targetLat', 'targetLng'])
        return processedData

    # maps grids data to nwp data i.e. for every source and target vessels it finds respective grids (id)
    def mapGridstoNWPData(self, nwpData, gridsData):
        try:
            nwpData.insert(10, 'sourceMstrId', '')
            nwpData.insert(11, 'targetMstrId', '')
            nwpData.insert(12, 'sourceContains', False) # flag in dataframe for source MMSI to avoid over-write
            nwpData.insert(13, 'targetContains', False) # flag in dataframe for target MMSI to avoid over-write

            for i in nwpData.index:
                sourcePoint = Point(float(nwpData['sourceLat'][i]), float(nwpData['sourceLng'][i])) # single source MMSI location
                targetPoint = Point(float(nwpData['targetLat'][i]), float(nwpData['targetLng'][i])) # single target MMSI location

                for j in gridsData.index:
                    singleCell = wkb.loads(gridsData['geom'][j], hex=True)

                    # checking if grid cell contains source MMSI
                    if nwpData['sourceContains'][i] == False:
                        if singleCell.contains(sourcePoint) == True:
                            nwpData.loc[i, 'sourceContains'] = True
                            nwpData.loc[i, 'sourceMstrId'] = gridsData['mstrid'][j]

                    # checking if grid cell contains target MMSI
                    if nwpData['targetContains'][i] == False:
                        if singleCell.contains(targetPoint) == True:
                            nwpData.loc[i, 'targetContains'] = True
                            nwpData.loc[i, 'targetMstrId'] = gridsData['mstrid'][j]

            del nwpData['sourceContains']
            del nwpData['targetContains']
        except Exception as e:
            print(e)
        return nwpData

    # prepare graph for calculation so that we can calculate distance with Djikstra or Floyd-Warshall
    def prepareGraph(self, **kwargs):
        # filepath: distance calculation data generated with QGIS and processed grids, first centroid were calculated
        #           then one to six point distance matrix generated, set file path with 'filepath'.
        self.filePath = kwargs.get('filepath','../Data/DistanceMatrix/oneToSixPoints_10x10.csv')
        graph = Graph.Graph()
        csvToMatrix = CSVtoMatrix.CSVtoMatrix(self.filePath)
        gridsData = csvToMatrix.inputData()

        # adding edges for graph i.e. nodes, distance
        for i in gridsData.index:
            graph.addEdge(gridsData['InputID'][i], gridsData['TargetID'][i], gridsData['Distance'][i])
        return graph

    # Instantiate Djikstra, which finds minimum distance and path given source and target nodes and graph.
    def calculateDistance(self, graph, source, target):
        djikstra = Djikstra.Djikstra(graph, source, target)
        path, distance = djikstra.djikstra()
        return path, distance


    def processedNWPDataCalculation(self, mappedNWPData):
        try:
            mappedNWPData.insert(13, 'distance', '')
            mappedNWPData.insert(14, 'minimum', '')
            mappedNWPData.insert(15, 'predictedPath', '')
            graph = self.prepareGraph()

            # finding distance
            for i in mappedNWPData.index:
                path, distance = self.calculateDistance(graph, mappedNWPData['sourceMstrId'][i], mappedNWPData['targetMstrId'][i])
                mappedNWPData.loc[i, 'distance'] = float(distance)/1000
                mappedNWPData.loc[i, 'predictedPath'] = path

            # finding minimum distance: for a vessel on given date and on given time, sets 'minimum' column True
            uniqueSourceMMSI = list(set(mappedNWPData['sourceMMSI'].values.tolist()))
            for i in range(0, len(uniqueSourceMMSI)):
                tempDataFrame = mappedNWPData.loc[mappedNWPData['sourceMMSI'] == uniqueSourceMMSI[i]]
                uniqueDate = list(set(tempDataFrame['sourceDate'].values.tolist()))

                for j in range(0, len(uniqueDate)):
                    tempDataFrame = tempDataFrame.loc[tempDataFrame['sourceDate'] == uniqueDate[j]]
                    uniqueTime = list(set(tempDataFrame['sourceTime'].values.tolist()))

                    for k in range(0, len(uniqueTime)):
                        tempDataFrame = tempDataFrame.loc[tempDataFrame['sourceTime'] == uniqueTime[k]]
                        distance = list(set(tempDataFrame['distance'].values.tolist()))
                        minDistance = min(distance)
                        mappedNWPData.loc[tempDataFrame.index[tempDataFrame['distance'] == minDistance], 'minimum'] = True

        except Exception as e:
            print(e)
        return mappedNWPData
