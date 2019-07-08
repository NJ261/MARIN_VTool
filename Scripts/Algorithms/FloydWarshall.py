#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 17:22:05 2019

@author: nirav
"""
INF = 100000000000 # infinite stage

def floydWarshall(vertex, adjacencyMatrix):
    for k in range(0, vertex):
        for i in range(0, vertex):
            for j in range(0, vertex):
                # compare possible paths with the current value in matrix and update matrix with minimum value
                adjacencyMatrix[i][j] = min(adjacencyMatrix[i][j], adjacencyMatrix[i][k] + adjacencyMatrix[k][j])

    return adjacencyMatrix

# to print floyd warshall result in matrix format
def printMatrix(vertex, adjacencyMatrix):
    for i in range(0, vertex):
        print("\t {:d}".format(i+1), end='') # top row for headers
    print();
    for i in range(0, vertex):
        print("{:d}".format(i+1), end='') # first left column as headers
        for j in range(0,vertex):
            print("\t{:2d}".format(adjacencyMatrix[i][j]), end='')
        print()


# inputMatrix as in list of list format, mentioned below.
inputMatrix = [[0,3,6,INF,INF,INF,INF],
                [3,0,2,1,INF,INF,INF],
                [6,2,0,1,4,2,INF],
                [INF,1,1,0,2,INF,4],
                [INF,INF,4,2,0,2,1],
                [INF,INF,2,INF,2,0,1],
                [INF,INF,INF,4,1,1,0]
]
vertex = 7

adjacencyMatrix = floydWarshall(vertex, inputMatrix);
printMatrix(vertex, adjacencyMatrix)


