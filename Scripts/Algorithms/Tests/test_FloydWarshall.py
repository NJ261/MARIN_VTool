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

class TestFloydWarshall(unittest.TestCase):

    def setUp(self):
        self.vertex = 3
        self.infiniteStage = 1000000000
        self.inputData = [[0, 1, 2], [1, 0, self.infiniteStage], [2, self.infiniteStage, 0]]
        self.outputData = [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
        self.floydWarshall = FloydWarshall.FloydWarshall(self.vertex, self.inputData)

    def test_matrixConversion(self):
        self.assertEquals(self.floydWarshall.floydWarshall(), self.outputData)

    @patch('FloydWarshall.FloydWarshall.printMatrix')
    def test_inputData(self, mock_printMatrix):
        mock_printMatrix.return_value = 'Success'
        self.assertEqual(self.floydWarshall.printMatrix(), 'Success')

if __name__ == '__main__':
    unittest.main()