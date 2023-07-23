from pysnmp.hlapi import *
import os
import time 
from datetime import datetime
import numpy as np


class PSU():
    '''
    This class represents the template for power supplies such as mpods, TTIs, etc.
    '''
    def __init__(self, module, unit, miblib='./mibs/'):
        '''
        Power supply (PSU) constructor
        '''
        self.module = module
        self.unit = unit
        self.miblib = miblib

    