#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 7/12/19 1:11 PM

@author: nirav
"""
import subprocess
import ReadXMLConfigData

class SSHTunnel:
    '''
    Description:
    ------------
    Start SSH tunnel connection

    Parameters:
    -----------
    **kwargs :
             inputFile : input xml file for config data i.e. 'Config/SampleSSHConfig.xml'
    '''

    def __init__(self, inputFile):
        self.inputFile = inputFile
        self.configData = ReadXMLConfigData.ReadXMLConfigData(self.inputFile).readXMLData()
        self.userName = self.configData[0][1]
        self.host = self.configData[1][1]
        self.localPort = self.configData[2][1]
        self.remotePort = self.configData[3][1]

    def startTunnel(self):
        commandString1 = "{}:localhost:{}".format(self.localPort, self.remotePort)
        commandString2 = "{}@{}".format(self.userName, self.host)
        sshSubprocess = subprocess.Popen(["ssh", "-L", commandString1, commandString2],
                                         shell=False,   # keep shell=False for preventing backdoor access
                                         stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
        return sshSubprocess

    def stopTunnel(self, sshSubprocess):
        sshSubprocess.communicate()
        sshSubprocess.kill()
        return print('Subprocess is stopped')
