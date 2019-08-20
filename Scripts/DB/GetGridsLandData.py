#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 8/15/19 12:46 AM

@author: nirav
"""
import pandas as pd
import DBConnection

class GetGridsLandData:

    def __init__(self, **kwargs):
        self.dbConfigFile = kwargs.get('fileName','../DB/Config/DBConfig.xml')
        self.dbConnection = DBConnection.DBConnection(self.dbConfigFile)

    def getLandData(self):
        landData = []
        #countryList = ['ca', 'us', 'gl']
        countryList = ['ca']
        connection = self.dbConnection.getConnection()
        cursor = connection.cursor()

        for country in countryList:
            cursor.execute("select ogc_fid, wkb_geometry from cp_coast_la where country = '{}';".format(country))
            for row in cursor:
                landData.append(row)

        self.dbConnection.closeConnection(cursor, connection)
        landData = pd.DataFrame(landData, columns=['id','geom'])
        return landData


    def getGridsData(self):
        gridsData = []
        connection = self.dbConnection.getConnection()
        cursor = connection.cursor()

        cursor.execute("select id, mstrid, grid0_1, geom from amtgrids limit 1000 offset 9000;")
        for row in cursor:
            gridsData.append(row)

        self.dbConnection.closeConnection(cursor, connection)
        gridsData = pd.DataFrame(gridsData, columns=['id','mstrid','grid0_1','geom'])
        return gridsData