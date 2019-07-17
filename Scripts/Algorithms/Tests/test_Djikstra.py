#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 7/16/19 10:58 PM

@author: nirav
"""
import sys
sys.path.insert(0, '../../')

import unittest

from Algorithms.Djikstra import Djikstra
from DataProcessing.Graph import Graph

class TestDjikstra(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()
        self.inputData = [('A','B',1),('A','C',3),('C','D',1),('B','D',1)]
        for edge in self.inputData: self.graph.addEdge(*edge)
        self.outputData = ['A', 'B', 'D']
        self.djikstra = Djikstra(self.graph, 'A', 'D')

    def test_djikstra(self):
        self.assertEquals(self.djikstra.djikstra(), self.outputData)

if __name__ == '__main__':
    unittest.main()
