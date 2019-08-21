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

    def __init__(self, grids, landArea, **kwargs):
        self.grids = grids.copy()
        self.landArea = landArea.copy()
        self.gridsTargetCol = kwargs.get('gridsCol', 'geom')
        self.landAreaTargetCol = kwargs.get('landAreaCol','geom')
        self.sourceCRS = kwargs.get('sourceCRS', 'epsg:3571')
        self.destinationCRS = kwargs.get('destCRS', 'epsg:4269')
        self.project = partial(pyproj.transform,
                               pyproj.Proj(init=self.sourceCRS), #source co-ordinate system
                               pyproj.Proj(init=self.destinationCRS)) # destination co-ordinate system

    def removeLandFromGridCells(self):
        try:
            self.grids.insert(3, 'intersect', False)
            for j in self.grids.index:
                singleGridCell = wkb.loads(self.grids[self.gridsTargetCol][j], hex=True) # reading a grid cell in wkb format as a polygon

                for i in self.landArea.index:
                    singlePolygon = wkb.loads(self.landArea[self.landAreaTargetCol][i], hex=True)  # reading co-ordinates in wkb format as a polygon
                    singlePolygon = transform(self.project, singlePolygon)  # changing land polygon's CRS to match with grid's CRS
                    if self.grids['intersect'][j] == False:

                        # check if grid cell and polygon intercet or not, if yes then it will find difference.
                        if singleGridCell.intersects(singlePolygon) == True:
                            self.grids.loc[j, 'intersect'] = True
                            difference = singleGridCell.difference(singlePolygon)
                            try:
                                # if difference have more than 1 polygons, it will consider the one which has larger area and drop rest.
                                if len(difference) >= 1:
                                    self.grids.loc[j, self.gridsTargetCol] = difference[difference.index(max(difference))].wkb_hex
                            except:
                                # case: where difference has only 1 polygon, it will update it
                                self.grids.loc[j, self.gridsTargetCol] = difference.wkb_hex
                        else:
                            self.grids.loc[j, self.gridsTargetCol] = self.grids[self.gridsTargetCol][j]

        except Exception as e:
            print(e)

        return self.grids