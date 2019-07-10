#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 7/10/19 2:48 PM

@author: nirav
"""

from shapely.geometry import Point
import pyproj

class DistanceMatrix:
    '''
    Description:
    ------------
    Calculate distance matrix based on one matrix / two matrices (great circle distance in KM)

    Parameters:
    -----------
    **kwargs :
             projection : set projection by default it is 'WGS84'.
    '''

    def __init__(self, **kwargs):
        self.projection = kwargs.get('projection','WGS84')

    def distanceMatrixCalculation(self, inputMatrixA, **kwargs):
        '''
        Description:
        ------------
        Calculate distance matrix based on input.
            1. calculate matrix against single matrix.
                e.g. distanceMatrixCalculation(inputData)

            2. calculate distance matrix against 2 metrices.
                e.g. distanceMatrixCalculation(inputDataA, inputMatrixB=inputDataB)

        Parameters:
        -----------
        inputMatrixA,
        **kwargs :
             inputMatrixB : second matrix for distance calculation

        Here, all matrix input should be in list of list e.g. [[long1,lat1],[long2,lat2]]

        Returns:
        --------
        Distance matrix in list of list format
        '''
        self.inputMatrixB = kwargs.get('inputMatrixB', inputMatrixA)
        geod = pyproj.Geod(ellps=self.projection)
        processedData, tempData = [], []

        for i in range(0, len(inputMatrixA)):
            point1 = Point(inputMatrixA[i][0], inputMatrixA[i][1])

            for j in range(0, len(self.inputMatrixB)):
                point2 = Point(self.inputMatrixB[j][0], self.inputMatrixB[j][1])
                angle1, angle2, distance = geod.inv(point1.x, point1.y, point2.x, point2.y)
                tempData.append(float('{:.2f}'.format(distance / 1000))) # distance in KM

            processedData.append(tempData)
            tempData = []
        return processedData
