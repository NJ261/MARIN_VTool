#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 7/16/19 10:58 PM

@author: nirav
"""
from collections import defaultdict

class Graph:

    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}

    def addEdge(self, fromNode, toNode, weight):
        self.edges[fromNode].append(toNode)
        self.edges[toNode].append(fromNode)
        self.weights[(fromNode, toNode)] = weight
        self.weights[(toNode, fromNode)] = weight