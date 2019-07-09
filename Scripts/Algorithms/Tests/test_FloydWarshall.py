#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 7/9/19 8:25 PM

@author: nirav
"""
import sys
sys.path.insert(0, '../')

import unittest
from unittest.mock import patch

import FloydWarshall
vertex = 3
infiniteStage = 1000000000
inputData = [[0,1,2],[1,0,infiniteStage],[2,infiniteStage,0]]
outputData = [[0,1,2],[1,0,3],[2,3,0]]
floydWarshall = FloydWarshall.FloydWarshall(vertex, inputData)

class TestFloydWarshall(unittest.TestCase):

    def test_matrixConversion(self):
        self.assertEquals(floydWarshall.floydWarshall(), outputData)

    @patch('FloydWarshall.FloydWarshall.printMatrix')
    def test_inputData(self, mock_printMatrix):
        mock_printMatrix.return_value = 'Success'
        self.assertEqual(floydWarshall.printMatrix(), 'Success')

if __name__ == '__main__':
    unittest.main()