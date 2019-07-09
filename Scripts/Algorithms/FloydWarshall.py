#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 17:22:05 2019

@author: nirav
"""

class FloydWarshall:
    '''
    Description:
    ------------
    runs floydwarshall algorithm and print the result in matrix form

    Parameters:
    -----------
    self,
    vertex : number of vertexes
    adjacencyMatrix: input matrix should be in list of list form, containing infinite stage as very high number.
                    [[0,1,2],
                     [1,0,inf],
                     [2,inf,0]] where inf=10000000000
    '''

    def __init__(self, vertex, adjacencyMatrix):
        self.vertex = vertex
        self.adjacencyMatrix = adjacencyMatrix

    def floydWarshall(self):
        for k in range(0, self.vertex):
            for i in range(0, self.vertex):
                for j in range(0, self.vertex):
                    # compare possible paths with the current value in matrix and update matrix with minimum value
                    self.adjacencyMatrix[i][j] = min(self.adjacencyMatrix[i][j], self.adjacencyMatrix[i][k] + self.adjacencyMatrix[k][j])
        return self.adjacencyMatrix

    # to print floyd warshall result in matrix format
    def printMatrix(self):
        for i in range(0, self.vertex):
            print("\t {:d}".format(i+1), end='') # top row for headers
        print();
        for i in range(0, self.vertex):
            print("{:d}".format(i+1), end='') # first left column as headers
            for j in range(0,self.vertex):
                print("\t{:2d}".format(self.adjacencyMatrix[i][j]), end='')
            print()
