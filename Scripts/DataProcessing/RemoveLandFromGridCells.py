#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 7/24/19 7:23 PM

@author: nirav
"""
from functools import partial
from shapely.ops import transform
from shapely import wkb
import pyproj

class RemoveLandFromGridCells:
    '''
    Description:
    ------------
    It removes land area from the grids

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
        self.sourceCRS = kwargs.get('sourceCRS', 'epsg:3571')
        self.destinationCRS = kwargs.get('destCRS', 'epsg:4269')
        self.project = partial(pyproj.transform,
                               pyproj.Proj(init=self.sourceCRS), #source co-ordinate system
                               pyproj.Proj(init=self.destinationCRS)) # destination co-ordinate system

    def removeLandFromGridCells(self, grids, landArea):
        gridsData = grids.copy()
        landData = landArea.copy()
        try:
            gridsData.insert(3, 'intersect', False)
            for j in gridsData.index:
                singleGridCell = wkb.loads(gridsData[self.gridsTargetCol][j], hex=True) # reading a grid cell in wkb format as a polygon

                for i in landData.index:
                    singlePolygon = wkb.loads(landData[self.landAreaTargetCol][i], hex=True)  # reading co-ordinates in wkb format as a polygon
                    singlePolygon = transform(self.project, singlePolygon)  # changing land polygon's CRS to match with grid's CRS
                    if gridsData['intersect'][j] == False:

                        # check if grid cell and polygon intercet or not, if yes then it will find difference.
                        if singleGridCell.intersects(singlePolygon) == True:
                            gridsData.loc[j, 'intersect'] = True
                            difference = singleGridCell.difference(singlePolygon)
                            try:
                                # if difference have more than 1 polygons, it will consider the one which has larger area and drop rest.
                                if len(difference) >= 1:
                                    gridsData.loc[j, self.gridsTargetCol] = difference[difference.index(max(difference))].wkb_hex
                            except:
                                # case: where difference has only 1 polygon, it will update it
                                gridsData.loc[j, self.gridsTargetCol] = difference.wkb_hex
                        else:
                            gridsData.loc[j, self.gridsTargetCol] = singleGridCell.wkb_hex

            del gridsData['intersect']
        except Exception as e:
            print(e)

        return gridsData