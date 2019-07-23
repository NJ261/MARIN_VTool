#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 7/16/19 10:58 PM

@author: nirav
"""
from collections import defaultdict

class Graph:

    def __init__(self):
        """
        self.edges: dict for possible nodes
                    e.g. {'A': ['B', 'C', 'D'], 'B': ['A', 'C']}
        self.weights: weights between two nodes (as a tuple)
                      and tuple as a key to weight.
                      e.g. {('A', 'B'): 3, ('A', 'C'): 4}
        """
        self.edges = defaultdict(list)
        self.weights = {}

    def addEdge(self, fromNode, toNode, weight):
        self.edges[fromNode].append(toNode)
        self.edges[toNode].append(fromNode)
        self.weights[(fromNode, toNode)] = weight
        self.weights[(toNode, fromNode)] = weight