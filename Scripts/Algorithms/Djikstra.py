#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 7/16/19 10:58 PM

@author: nirav
"""

class Djikstra:

    def __init__(self, graph, initialNode, endNode):
        self.graph = graph
        self.endNode = endNode
        self.shortestPath = {initialNode: (None, 0)}
        self.currentNode = initialNode
        self.visitedNode = set()
        self.path = []

    def djikstra(self):
        while self.currentNode != self.endNode:
            self.visitedNode.add(self.currentNode)
            neighbourNodes = self.graph.edges[self.currentNode]
            currentNodeWeight = self.shortestPath[self.currentNode][1]

            # searching through each neighbour
            for nextNode in neighbourNodes:
                weight = self.graph.weights[(self.currentNode, nextNode)] + currentNodeWeight
                if nextNode not in self.shortestPath:
                    self.shortestPath[nextNode] = (self.currentNode, weight)
                else:
                    currentShortestNodeWeight = self.shortestPath[nextNode][1]
                    if currentShortestNodeWeight > weight:
                        self.shortestPath[nextNode] = (self.currentNode, weight)

            # next neighbour node with lowest weight
            nextNeighbourNodes = {node: self.shortestPath[node] for node in self.shortestPath
                                                                if node not in self.visitedNode}
            if not nextNeighbourNodes:
                return print("Route is not possible.")

            self.currentNode = min(nextNeighbourNodes, key=lambda k: nextNeighbourNodes[k][1])

        # go back from destination to origin for shortest path
        while self.currentNode != None:
            self.path.append(self.currentNode)
            nextNode = self.shortestPath[self.currentNode][0]
            self.currentNode = nextNode

        return self.path[::-1] # reversing path