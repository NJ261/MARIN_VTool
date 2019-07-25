#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 7/24/19 6:54 PM

@author: nirav
"""
import sys
sys.path.insert(0, '../')

import unittest
from shapely.geometry import Polygon
import pandas


import RemoveLandFromGridCells

class TestRemoveLandFromGridCells(unittest.TestCase):

    def setUp(self):
        self.samplePolygon = pandas.DataFrame([Polygon([[0,0],[0,2],[1,0]]).wkb_hex], columns=['geom'])
        self.gridCell = pandas.DataFrame([Polygon([[0,0],[0,2],[2,2],[2,0]]).wkb_hex], columns=['geom'])
        self.gridCell2 = pandas.DataFrame([Polygon([[0,0],[0,2],[2,2],[2,0]]).wkb_hex], columns=['temp'])
        self.output = pandas.DataFrame([Polygon([[0,2],[2,2],[2,0],[1,0],[0,2]]).wkb_hex], columns=['geom'])
        self.removeLandFromGridCells = RemoveLandFromGridCells.RemoveLandFromGridCells(self.gridCell,
                                                                                       self.samplePolygon, sourceCRS='epsg:4269')
        self.removeLandFromGridCellsError = RemoveLandFromGridCells.RemoveLandFromGridCells(self.gridCell2,
                                                                                            self.samplePolygon, sourceCRS='epsg:4269')

    def test_removeLandFromGridCells(self):
        # here, comparing list instead of dataframes
        self.assertListEqual(self.removeLandFromGridCells.removeLandFromGridCells().values.tolist(),
                             self.output.values.tolist())

    def test_removeLandFromGridCellsError(self):
        # here, returned dataframe will be None if any error occurs (wrong target columns here)
        self.assertEquals(self.removeLandFromGridCellsError.removeLandFromGridCells(), None)

if __name__ == '__main__':
    unittest.main()
