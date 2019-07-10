#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 7/10/19 3:04 PM

@author: nirav
"""
import sys
sys.path.insert(0, '../')

import unittest
import DistanceMatrix
distanceMatrix = DistanceMatrix.DistanceMatrix()

class TestDistanceMatrix(unittest.TestCase):

    # mock data for test cases
    def setUp(self):
        self.inputDataA = [[-86.95, 74.45], [-86.85, 74.45]]
        self.inputDataB = [[-86.95, 74.35], [-86.85, 74.35]]

    def test_distanceMatrixCalculationSingleMatrix(self):
        self.assertEqual(distanceMatrix.distanceMatrixCalculation(self.inputDataA), [[0,2.99],[2.99,0]])

    def test_distanceMatrixCalculationDoubleMatrix(self):
        self.assertEqual(distanceMatrix.distanceMatrixCalculation(self.inputDataA, inputMatrixB=self.inputDataB),
                         [[11.16, 11.56], [11.56, 11.16]])

if __name__ == '__main__':
    unittest.main()
