### CSV to Matrix
convert csv data to the matrix form (e.g. from Table: A to Table: B)

```python
import CSVtoMatrix

# read csv file
csvtoMatrix = CSVtoMatrix.CSVtoMatrix('temp.csv')
inputData = csvtoMatrix.inputData() # inputData as pandas dataFrame

# matrix form
processedData = csvtoMatrix.matrixConversion(inputData)

# write matrix to csv
csvtoMatrix.writeDataToCSV(inputData)
```

Table: A 

| Row | Column | Value |
| :---: | :------: | :-----: |
| 1 | 2 | 20 |
| 1 | 3 | 30 |
| 2 | 1 | 20 |
| 2 | 3 | 50 |
| 3 | 1 | 30 |
| 3 | 2 | 50 |

Table: B

|  | 1 | 2 | 3 |
| :---: | :------: | :-----: |:-----: |
| 1 | 0 | 20 | 30 |
| 2 | 20 | 0 | 50 |
| 3 | 30 | 50 | 0 |

### Distance Matrix
Generate a distance matrix based on one matrix / two matrices.

Here, distance is in KM and input matrix should be in list of list format e.g. [[long1,lat1], [long2,lat2]]
```python
import DistanceMatrix

distanceMatrix = DistanceMatrix.DistanceMatrix()
inputDataA = [[-86.95, 74.45], [-86.85, 74.45]]
inputDataB = [[-86.95, 74.35], [-86.85, 74.35]]

# Single Matrix
outputData = distanceMatrix.distanceMatrixCalculation(inputDataA)

# Two Matrices
outputData = distanceMatrix.distanceMatrixCalculation(inputDataA, inputMatrixB=inputDataB)
```

### Graph
Create a graph for Dijkstra algorithm
```python
import Graph

graph = Graph()

# add node values to the graph
# For inputData: refer to the Data/DistanceMatrix/oneToSixPoints_10x10.csv
for i in range(0, len(inputData)):
    graph.addEdge(inputData['InputID'][i], inputData['TargetID'][i], inputData['Distance'][i])
```

### Remove land from grid cells
It removes land from on-shore cells and gives the water region.

Here, inputs should be in pandas dataframe (for grids and land data).
The output will be in pandas dataframe. Also, change CRS for land, it is 'epsg:3571' by default, change it with 'sourceCRS'.
```python
import RemoveLandFromGridCells

# geometry should be in wkb_hex format
land = '' # should be in pandas dataframe
grids = '' # should be in pandas dataframe
sourceCRS = 'epsg:4269' # changing CRS for lands

'''
**kwargs:
    1. gridsCol: target column for geometry data in grids, default value is 'geom'. 
    2. landAreaCol: target column for geometry data in land, default value is 'geom'.
    3. sourceCRS: CRS for land data, default CRS is 'epsg:3571'.
    4. destCRS: CRS for grids data, default CRS is 'epsg:4269'.
 
'''

removeLndFrmGrids = RemoveLandFromGridCells(grids, land, sourceCRS=sourceCRS)

# output as a pandas dataframe
processedGrids = removeLndFrmGrids.removeLandFromGridCells()
```