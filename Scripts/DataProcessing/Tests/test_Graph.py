#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 7/16/19 10:57 PM

@author: nirav
"""
import sys
sys.path.insert(0, '../')

import unittest
from collections import defaultdict

import Graph

class TestGraph(unittest.TestCase):

    def setUp(self):
        self.graph = Graph.Graph()
        self.inputData = [('A','B', 1), ('A','C', 2)]
        self.outputEdges = defaultdict(list, {'A': ['B', 'C'], 'B': ['A'], 'C': ['A']})
        self.outputWeights = {('A', 'B'): 1, ('B', 'A'): 1, ('A', 'C'): 2, ('C', 'A'): 2}

    def test_addEdge(self):
        for edge in self.inputData:
            self.graph.addEdge(*edge)
        self.assertEquals(self.graph.edges, self.outputEdges)
        self.assertEquals(self.graph.weights, self.outputWeights)

if __name__ == '__main__':
    unittest.main()
