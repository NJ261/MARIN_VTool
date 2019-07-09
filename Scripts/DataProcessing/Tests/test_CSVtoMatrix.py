import sys
sys.path.insert(0, '../')

import pandas as pd
import unittest
from unittest.mock import patch

import CSVtoMatrix
csvtoMatrix = CSVtoMatrix.CSVtoMatrix('temp')

class TestCSVtoMatrix(unittest.TestCase):

    @patch('CSVtoMatrix.CSVtoMatrix.inputData')
    def test_inputData(self, mock_inputData):
        mock_inputData.return_value = 'Success'
        self.assertEqual(csvtoMatrix.inputData(), 'Success')

    def test_matrixConversion(self):
        data = [[1, 2, 2000], [2, 1, 3000]]
        outputData = [[0, 2.00], [3.00, 0]]
        dataFrame = pd.DataFrame(data, columns=['InputID', 'TargetID', 'Distance'])
        self.assertEquals(csvtoMatrix.matrixConversion(dataFrame), outputData)

    @patch('CSVtoMatrix.CSVtoMatrix.writeDataToCSV')
    def test_writeDataToCSV(self, mock_writeDataToCSV):
        mock_writeDataToCSV.return_value = 'Success'
        self.assertEqual(csvtoMatrix.writeDataToCSV(), 'Success')

if __name__ == '__main__':
    unittest.main()
