#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 8/15/19 2:53 AM

@author: nirav
"""
import sys
sys.path.insert(0, '../DB/')

import pandas as pd
import GetNWPData, GetGridsLandData, NWPDataProcessing

class INWPDataProcessing:
    '''
    Description:
    ------------
    Interface for NWPDataProcessing class and perform operations
    '''

    def __init__(self):
        # Instantiate objects to get data from DB
        self.getNWPData = GetNWPData.GetNWPData()
        self.getGridsLandData = GetGridsLandData.GetGridsLandData()

    def iNWPDataProcessing(self):
        nwpData = self.getNWPData.getNWPData()
        communityData = self.getNWPData.getCommunityData()
        print('NWPDataProcessing Task: 1/5 completed')

        self.nwpDataProcessing = NWPDataProcessing.NWPDataProcessing()
        nwpData, uniqueMMSI = self.nwpDataProcessing.filterData(nwpData)
        print ('NWPDataProcessing Task: 2/5 completed')

        nwpData = self.nwpDataProcessing.convertLatLng(nwpData)
        print('NWPDataProcessing Task: 3/5 completed')

        nwpData = self.nwpDataProcessing.splitDateTime(nwpData)
        print('NWPDataProcessing Task: 4/5 completed')

        nwpData = self.nwpDataProcessing.sortValuesByDateTime(nwpData, uniqueMMSI, communityData)
        print('NWPDataProcessing Task: 5/5 completed')
        return nwpData

    # For mapping grids to processed NWP data
    def iMapGridstoNWPData(self, processedNWPData):
        #processedNWPData = self.getNWPData.getProcessedNWPdata()
        gridsData = self.getGridsLandData.getGridsData(tablename='processedgrids')
        mappedNWPData = self.nwpDataProcessing.mapGridstoNWPData(processedNWPData, gridsData)
        print('Mapping of Grids to NWP data completed')
        return mappedNWPData

    # For finding distance from mappedNWPData
    def iProcessedNWPDataCalculation(self, mappedNWPData):
        #mappedNWPData = self.getNWPData.getGridsMappedNWPData()
        nwpData = self.nwpDataProcessing.processedNWPDataCalculation(mappedNWPData)
        nwpData.to_csv('processedNWPDataCalculation.csv', sep=',', encoding='utf-8', index=False)
        print('Final NWP Data is ready, written in processedNWPData.csv file')


if __name__ == '__main__':
    iNWPDataProcessing = INWPDataProcessing()
    processedNWPData = iNWPDataProcessing.iNWPDataProcessing()
    processedNWPData.to_csv('processedNWPData.csv', sep=',', encoding='utf-8', index=False)
    print('processedNWPData.csv COMPLETED')

    mappedNWPData = iNWPDataProcessing.iMapGridstoNWPData(processedNWPData)
    mappedNWPData.to_csv('mappedNWPData.csv', sep=',', encoding='utf-8', index=False)
    print('mappedNWPData.csv COMPLETED')

    iNWPDataProcessing.iProcessedNWPDataCalculation(mappedNWPData)

