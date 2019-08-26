#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 7/12/19 1:11 PM

@author: nirav
"""
import psycopg2
import ReadXMLConfigData

class DBConnection:
    '''
    Description:
    ------------
    get DB connection from xml config file and also close DB connetion.

    Parameters:
    -----------
    **kwargs :
             inputFile : input xml file for DB connection i.e. 'Config/SampleDBConfig.xml'
    '''

    def __init__(self, inputFile):
        self.inputFile = inputFile
        self.configData = ReadXMLConfigData.ReadXMLConfigData(self.inputFile).readXMLData()
        self.host = self.configData[0][1]
        self.database = self.configData[1][1]
        self.user = self.configData[2][1]
        self.password = self.configData[3][1]
        self.port = self.configData[4][1]

    # get DB connection
    def getConnection(self):
        try:
            connection = psycopg2.connect(host=self.host, database=self.database,
                                          user=self.user, password=self.password,
                                          port=self.port)
        except psycopg2.Error as error:
            print(error)
            connection = None
        return connection

    # close DB connection
    def closeConnection(self, cursor, connection):
        cursor.close()
        connection.close()
        return print("DB Connection closed")
