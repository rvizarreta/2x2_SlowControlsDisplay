from pysnmp.hlapi import *
import os
import time 
from datetime import datetime
import numpy as np
from influxdb import InfluxDBClient
from configparser import ConfigParser

class PSU():
    '''
    This class represents the template for power supplies such as mpods, TTIs, etc.
    '''
    def __init__(self, module, unit):
        '''
        Power supply (PSU) constructor
        '''
        self.unit = unit
        self.module = module
    
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    # INFLUXDB METHODS
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    def InitializeInfluxDB(self):
        '''
        Create InfluxDB client
        '''
        conf = ConfigParser()
        conf.read("./config.ini")
        db = conf["DATABASE"]
        client = InfluxDBClient('localhost', db.get('PORT'), self.unit) 
        db_name = self.module + "_" + self.unit
        client.create_database(db_name)
        client.switch_database(db_name)
        return client 
    
    def JSON_setup(self, measurement, channel_name, status, fields):
            '''
            Inputs:         - Measurement (i.e. light)
                            - Channel name (i.e. VGA_12_POS)
                            - Status (i.e. OFF)
                            - Fields (i.e. Voltage & current)

            Outputs:        - JSON file ready to be added to InfluxDB

            Description:    Provides new timestamp ready to be added to InfluxDB
            '''
            json_payload = []
            data = {
                # Table name
                "measurement" : measurement, 
                # Organization tags
                "tags" : { 
                    "channel_name" : channel_name,
                    "status" : status
                },
                # Time stamp
                "time" : datetime.utcnow().strftime('%Y%m%d %H:%M:%S'),
                # Data fields 
                "fields" : dict(fields)
            }
            json_payload.append(data)
            return json_payload

    

