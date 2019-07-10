import sys
sys.path.insert(0, '../')

import pandas as pd
import unittest
from unittest.mock import patch

import CSVtoMatrix
csvtoMatrix = CSVtoMatrix.CSVtoMatrix('temp')

class TestCSVtoMatrix(unittest.TestCase):

    # mock data for test cases
    def setUp(self):
        self.inputData = pd.DataFrame([[1, 2, 2000], [2, 1, 3000]],
                                      columns=['InputID', 'TargetID', 'Distance'])
        self.outputData = [[0, 2.00], [3.00, 0]]

    @patch('CSVtoMatrix.CSVtoMatrix.inputData')
    def test_inputData(self, mock_inputData):
        mock_inputData.return_value = 'Success'
        self.assertEqual(csvtoMatrix.inputData(), 'Success')

    def test_matrixConversion(self):
        self.assertEquals(csvtoMatrix.matrixConversion(self.inputData), self.outputData)

    @patch('CSVtoMatrix.CSVtoMatrix.writeDataToCSV')
    def test_writeDataToCSV(self, mock_writeDataToCSV):
        mock_writeDataToCSV.return_value = 'Success'
        self.assertEqual(csvtoMatrix.writeDataToCSV(), 'Success')

if __name__ == '__main__':
    unittest.main()
