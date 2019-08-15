#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 8/15/19 2:53 AM

@author: nirav
"""
import sys
sys.path.insert(0, '../DB/')

import pandas as pd
import GetNWPData, NWPDataProcessing

class INWPDataProcessing:

    def __init__(self):
        self.getNWPData = GetNWPData.GetNWPData()

    def iNWPDataProcessing(self):
        nwpData = self.getNWPData.getNWPData()
        print(len(nwpData))
        print('Task: 1/5 completed')

        self.nwpDataProcessing = NWPDataProcessing.NWPDataProcessing()
        nwpData, uniqueMMSI = self.nwpDataProcessing.filterData(nwpData)
        print(len(nwpData), len(uniqueMMSI))
        print ('Task: 2/5 completed')

        nwpData = self.nwpDataProcessing.convertLatLng(nwpData)
        print(len(nwpData))
        print('Task: 3/5 completed')

        nwpData = self.nwpDataProcessing.splitDateTime(nwpData)
        print(len(nwpData))
        print('Task: 4/5 completed')

        nwpData = self.nwpDataProcessing.sortValuesByDateTime(nwpData, uniqueMMSI)
        print(len(nwpData))
        nwpData.to_csv('nwpData.csv', sep=',', encoding='utf-8', index=False)
        print('Task: 5/5 completed')

if __name__ == '__main__':
    iNWPDataProcessing = INWPDataProcessing()
    iNWPDataProcessing.iNWPDataProcessing()

