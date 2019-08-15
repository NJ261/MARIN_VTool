#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 8/15/19 2:15 AM

@author: nirav
"""
import pandas as pd
import DBConnection

class GetNWPData:

    def __init__(self, **kwargs):
        self.dbConfigFile = kwargs.get('fileName', '../DB/Config/DBConfig.xml')
        self.dbConnection = DBConnection.DBConnection(self.dbConfigFile)

    def getNWPData(self):
        nwpData = []
        connection = self.dbConnection.getConnection()
        cursor = connection.cursor()

        cursor.execute("select mmsi, elp_sec, st_date, geom from nwp_ais_requestm1231827_201809_in_aoi_90min_seg_lines where length(mmsi) = 9;")
        for row in cursor:
            nwpData.append(row)

        self.dbConnection.closeConnection(cursor, connection)
        nwpData = pd.DataFrame(nwpData, columns=['mmsi', 'elp_sec', 'st_date', 'geom'])
        return nwpData