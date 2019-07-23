#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 7/12/19 1:11 PM

@author: nirav
"""
import sys
sys.path.insert(0, '../')

import unittest
from unittest.mock import patch

import DBConnection

class TestDBConnection(unittest.TestCase):

    def setUp(self):
        self.dbConnection = DBConnection.DBConnection('../Config/SampleDBConfig.xml')

    @patch('DBConnection.DBConnection.getConnection')
    def test_getConnection(self, mock_getConnection):
        mock_getConnection.return_value = 'Success'
        self.assertEquals(self.dbConnection.getConnection(), 'Success')

    def test_getConnectionError(self):
        self.assertEquals(self.dbConnection.getConnection(), None)

    @patch('DBConnection.DBConnection.closeConnection')
    def test_closeConnection(self, mock_closeConnection):
        mock_closeConnection.return_value = 'Success'
        self.assertEquals(self.dbConnection.closeConnection(), 'Success')

if __name__ == '__main__':
    unittest.main()
