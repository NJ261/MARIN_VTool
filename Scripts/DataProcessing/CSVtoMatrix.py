#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu July 8 14:05:39 2019

@author: nirav
"""
import pandas as pd

class CSVtoMatrix:

    def __init__(self, filePath):
        self.filePath = filePath

    # read input csv file
    def inputData(self):
        #filePath = '../../../distance_temp.csv'
        data = pd.read_csv(self.filePath)
        return data

    # conversion to matrix form function
    def matrixConversion(self, data):
        inputList = list(set(data['InputID'])) # set of unique input IDs
        processedData, tempData = [], []

        for i in range(0, len(inputList)):
            for j in range(0, len(data)):
                if int(inputList[i]) == int(data['InputID'][j]):
                    # normalizing distance here by the factor of 1000
                    tempData.append(float('{:.2f}'.format((data['Distance'][j])/1000)))
            processedData.append(tempData)
            processedData[i].insert(i,0) # insert 0 diagonally
            tempData = []

        return processedData

    # write matrix dataframe to csv
    def writeDataToCSV(self, data):
        dataFrame = pd.DataFrame(data)
        dataFrame.to_csv('CSVtoMatrix.csv', sep=',', encoding='utf-8', index=False, header=False)
        print('Writing to CSV file task completed')
