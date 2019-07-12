#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 7/12/19 1:11 PM

@author: nirav
"""
import sys
sys.path.insert(0, '../')

import unittest
from unittest.mock import patch

import SSHTunnel

class TestSSHTunnel(unittest.TestCase):

    def setUp(self):
        self.sshTunnel = SSHTunnel.SSHTunnel('../Config/SampleSSHConfig.xml')
        self.stopTunnelMsg = 'Subprocess is stopped'

    @patch('SSHTunnel.SSHTunnel.startTunnel')
    def test_startTunnel(self, mock_sshTunnel):
        mock_sshTunnel.return_value = 'Success'
        self.assertEqual(self.sshTunnel.startTunnel(), 'Success')

    @patch('SSHTunnel.SSHTunnel.stopTunnel')
    def test_stopTunnel(self, mock_stopTunnel):
        mock_stopTunnel.return_value = 'Success'
        tempSSHTunnel = self.sshTunnel.startTunnel()
        self.assertEquals(self.sshTunnel.stopTunnel(tempSSHTunnel), 'Success')

if __name__ == '__main__':
    unittest.main()
