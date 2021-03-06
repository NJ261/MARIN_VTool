#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 8/15/19 2:15 AM

@author: nirav
"""
import pandas as pd
import DBConnection

class GetNWPData:
    '''
    Description:
    ------------
    It gets land, grids data from DB and CSV file.

    Note: make sure DB config file is set
    '''

    def __init__(self, **kwargs):
        self.dbConfigFile = kwargs.get('fileName', '../DB/Config/DBConfig.xml')
        self.dbConnection = DBConnection.DBConnection(self.dbConfigFile)

    # get NWP data from db
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

    # get processed NWP data from DB
    def getProcessedNWPdata(self):
        nwpData = []
        connection = self.dbConnection.getConnection()
        cursor = connection.cursor()

        cursor.execute("select * from processednwpdata limit 500 offset 5000;")
        for row in cursor:
            nwpData.append(row)

        self.dbConnection.closeConnection(cursor, connection)
        columns = ['ogc_fid', 'sourceMMSI', 'targetMMSI', 'sourceDate', 'sourceTime', 'targetDate',
                   'targetTime', 'sourceLat', 'sourceLng', 'targetLat', 'targetLng']
        nwpData = pd.DataFrame(nwpData, columns=columns)
        return nwpData

    # get grids mapped NWP data
    def getGridsMappedNWPData(self):
        mappedNWPData = []
        connection = self.dbConnection.getConnection()
        cursor = connection.cursor()

        cursor.execute("select * from nwp_data;")
        for row in cursor:
            mappedNWPData.append(row)

        self.dbConnection.closeConnection(cursor, connection)
        columns = ['ogc_fid', 'sourceMMSI', 'targetMMSI', 'sourceDate', 'sourceTime', 'targetDate', 'targetTime',
                   'sourceLat', 'sourceLng', 'targetLat', 'targetLng', 'sourceMstrId', 'targetMstrId']
        mappedNWPData = pd.DataFrame(mappedNWPData, columns=columns)
        return mappedNWPData

    # get community data
    def getCommunityData(self):
        communityData = []
        connection = self.dbConnection.getConnection()
        cursor = connection.cursor()

        cursor.execute("select id, name, geom from communities;")
        for row in cursor:
            communityData.append(row)

        self.dbConnection.closeConnection(cursor, connection)
        columns = ['id', 'name', 'geom']
        communityData = pd.DataFrame(communityData, columns=columns)
        return communityData