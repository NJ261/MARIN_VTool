#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 8/15/19 12:38 AM

@author: nirav
"""
import sys
sys.path.insert(0, '../DB/')

import pandas as pd
import GetGridsLandData, RemoveLandFromGridCells

class IRemoveLandFromGridCells:

    def __init__(self):
        self.getGridsLandData = GetGridsLandData.GetGridsLandData()

    def iRemoveLandFromGridCells(self):
        gridsData = self.getGridsLandData.getGridsData()
        landData = self.getGridsLandData.getLandData()
        self.removeLandFromGridCells = RemoveLandFromGridCells.RemoveLandFromGridCells(gridsData, landData)
        gridsData = self.removeLandFromGridCells.removeLandFromGridCells()
        print (gridsData == self.getGridsLandData.getGridsData())
        return gridsData

if __name__ == '__main__':
    iRemoveLandFromGridCells = IRemoveLandFromGridCells()
    gridsData = iRemoveLandFromGridCells.iRemoveLandFromGridCells()
    gridsData.to_csv('processedGrids.csv', sep=',', encoding='utf-8', index=False)
