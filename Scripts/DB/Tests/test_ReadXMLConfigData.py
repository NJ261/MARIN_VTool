#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 7/12/19 7:08 PM

@author: nirav
"""
import sys
sys.path.insert(0, '../')

import unittest

import ReadXMLConfigData

class TestReadXMLConfigData(unittest.TestCase):

    def setUp(self):
        self.readXMLConfigData = ReadXMLConfigData.ReadXMLConfigData('../Config/SampleSSHConfig.xml')
        self.readXMLConfigDataError = ReadXMLConfigData.ReadXMLConfigData('mockData')
        self.outputData = [['username', 'temp'],['host', 'temp.com'],
                           ['localPort', '5433'],['remotePort', '5433']]
        self.error = 'Something wrong with file or file attributes'

    def test_readXMLData(self):
        self.assertEquals(self.readXMLConfigData.readXMLData(), self.outputData)

    def test_readXMLDataError(self):
        self.assertEquals(self.readXMLConfigDataError.readXMLData(), self.error)

if __name__ == '__main__':
    unittest.main()
