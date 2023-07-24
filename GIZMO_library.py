from PSU_library import PSU
import time 
from datetime import datetime
import numpy as np
from influxdb import InfluxDBClient
from configparser import ConfigParser
import paramiko
import warnings 
import traceback
import sys
warnings.filterwarnings(action='ignore',module='.*paramiko.*')
#from paramiko.py3compat import input

class GIZMO(PSU):
    '''
    This class represents the template for an MPOD.
    '''
    def __init__(self, module, unit, dict_unit, miblib='./mibs/'):
        '''
        Power supply (PSU) constructor
        '''
        self.miblib = miblib
        self.dictionary = dict_unit
        super().__init__(module, unit)

    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # MEASURING METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def measure(self):
        #conf = ConfigParser()
        #conf.read("./config.ini")
        #db = conf["GIZMO"]
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.dictionary["host-name"], self.dictionary["port"], self.dictionary["username"], self.dictionary["password"])
        chan = client.invoke_shell()
        chan.send('./GIZMO.elf 1\n')
        line = chan.recv(1000).decode('ASCII').strip()
        #chan.close()
        #client.close()
        return line

    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # INFLUXDB METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def INFLUX_write(self, powering, data):
        '''
        Inputs:         - Powering (i.e. resistance)
                        - Data (measurement value)

        Description:    Record timestamp on InfluxDB
        '''
        client = self.InitializeInfluxDB()
        client.write_points(self.JSON_setup(
            measurement = powering,
            fields = {
                powering : data
            }
        ))
        client.close()

    def CONTINUOUS_monitoring(self):
        '''
        Description:    Continuously record timestamp on InfluxDB
        '''
        powering_list = self.dictionary["powering"].keys()
        try:
            print('~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#')
            print("Continuous DAQ Activated")
            print("Taking data in real time")
            print('~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#')
            while True:
                line = self.measure()
                if 'RES' == line[0:3]:
                    line = line.replace('(', ' ')
                    line = line.replace(')', ' ')
                    line = line.replace('= ', '=')
                    line = line.replace(', ', ' ')
                    sl = line.split() # split line
                    print(sl)
                    data = [float(sl[i].split('=')[1]) for i in range(0,5)]
                    print(data)
                
                    for powering, value in zip(powering_list, data):
                        self.INFLUX_write(powering, value)
                
                    time.sleep(2)

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            sys.exit(1)