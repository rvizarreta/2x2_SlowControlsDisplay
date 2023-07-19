from pysnmp.hlapi import *
import os
import time 
from datetime import datetime

import numpy as np

class mpodPsu():
    
    def __init__(self,ip = ['192.168.196.6','192.168.196.7'], miblib='./mibs/'):
        self.ip = ['192.168.196.6','192.168.196.7']
        self.miblib = miblib

    def walk(self, mpodn):
        os.popen("snmpwalk -v 2c -M " + self.miblib +" -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " [OID]")
        ret = data.read().split('\n')

        return ret
    def list_defined(self):
        functions = dir(mpodPsu)
        usable = []
        for i in functions:
            if i[0:2]!="__":
                usable += [i]
        print(usable)
        
    def wtf_is(self,command):
        try:
            data = os.popen("grep -A6 "+command+" mpod_library.py | grep ' + '")
            ret = data.read().split('+')
            translation = os.popen("snmptranslate -On -Td -M /home/acd/acdemo/MPODs/mibs/ WIENER-CRATE-MIB::"+str(ret[5][3:-2]))
            return translation.read()
        except:
            return "Not an snmp command"
    
    def write_log(self):
        channels = [".u0", ".u1", ".u2", ".u3", ".u100", ".u101", ".u102", ".u103", ".u104", ".u105", ".u106", ".u107", ".u200", ".u201", ".u202", ".u203", ".u204", ".u205", ".u206", ".u207"]
        f = open("Historical.log", "a")
        f.write(str(datetime.now()) + "\n")
        for mpodn in [0]:
            mpod = mpodPsu(self.ip[mpodn])
            log_data = mpod.measure(mpodn,channels)
            for i in range(len(log_data[0])):
                print(str(channels[i]) +"\t"+ str(log_data[0][i]) + "\t" + str(log_data[1][i]) + " V \t" + str(log_data[2][i]) + " A\n")
                f.write(str(channels[i]) +"\t"+ str(log_data[0][i]) + "\t" + str(log_data[1][i]) + " V \t" + str(log_data[2][i]) + " A\n")
        f.close()
# Power switches

    def mpodSwitch(self, mpodn, switch):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[mpodn] + " sysMainSwitch" + ".0 i " + str(switch))

    #	Individual Channel Switch
    def channelSwitch(self, mpodn, switch, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[mpodn] + " outputSwitch" + channel + " i " + str(switch))
	
# Get commands:

    #	Retruns the status of the output channel
    def getStatus(self, mpodn, channel):

        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " outputStatus" + channel)
        ret = data.read().split('\n')

        return ret

    #	Returns the voltage that the channel was set to
    def getVoltage(self, mpodn, channel):

        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " outputVoltage" + channel)
        ret = data.read().split('\n')

        return ret[0].split(" ")[-2]

    #	Returns the current that the channel was set to
    def getCurrent(self, mpodn, channel):

        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " outputCurrent" + channel)
        ret = data.read().split('\n')

        return ret[0].split(" ")[-2]

    def behavior(self, mpodn, channel):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " outputSupervisionBehavior" + channel)
        ret = data.read().split('\n')

        return ret
    
    def getOutputNumber(self, mpodn):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " outputNumber" + ".0") 
        ret = data.read().split('\n')
        
        return ret

    def getgroupsNumber(self, mpodn):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " groupsNumber" + ".0")
        ret = data.read().split('\n')

        return ret    

    def getOutputName(self, mpodn,channel):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " outputName"+channel)
        ret = data.read().split('\n')

        return ret

    def getOutputGroup(self, mpodn, channel):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " outputGroup" + channel)
        ret = data.read().split('\n')

        return ret

    def getOutputConfigMaxSenseVoltage(self, mpodn, channel):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " outputConfigMaxSenseVoltage" + channel)
        ret = data.read().split('\n')

        return ret

    def getOutputConfigMaxTerminalVoltage(self, mpodn, channel):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " outputConfigMaxTerminalVoltage" + channel)
        ret = data.read().split('\n')

        return ret

    def getOutputConfigMaxCurrent(self, mpodn, channel):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " outputConfigMaxCurrent" + channel)
        ret = data.read().split('\n')

        return ret

    def getOutputConfigMaxPower(self, mpodn, channel):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " outputConfigMaxPower" + channel)
        ret = data.read().split('\n')

        return ret

    def getsensorNumber(self, mpodn):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " sensorNumber")
        ret = data.read().split('\n')

        return ret

    def getpsFirmwareVersion(self, mpodn):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " psFirmwareVersion" + ".0")
        ret = data.read().split('\n')

        return ret

    def getpsSerialNumber(self, mpodn):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " psSerialNumber" + ".0")
        ret = data.read().split('\n')

        return ret

    def getpsOperatingTime(self, mpodn):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " psOperatingTime" + ".0")
        ret = data.read().split('\n')

        return ret

    def getFanNominalSpeed(self,mpodn):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " fanNominalSpeed" + ".0")
        ret = data.read().split('\n')

        return ret

    def getfanFirmwareVersion(self, mpodn, channel):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " fanFirmwareVersion" + chanel)
        ret = data.read().split('\n')

        return ret

    def getfanSerialNumber(self, mpodn, channel):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " fanSerialNumber" + chanel)
        ret = data.read().split('\n')

        return ret

    def getfanOperatingTime(self, mpodn, channel):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " fanOperatingTime" + chanel)
        ret = data.read().split('\n')

        return ret

    def getfanAirTemperature(self, mpodn, channel):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " fanAirTemperature" + chanel)
        ret = data.read().split('\n')

        return ret

    def getfanNumberOfFans(self, mpodn):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " fanNumberOfFans")
        ret = data.read().split('\n')

        return ret

    def getfanSpeed(self, mpodn, fan):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " fanSpeed"+fan)
        ret = data.read()

        return ret

    """
    TM 17.02.2023
    get(current/voltage) gets the set value
    getMeasurement______(current/voltage) gets real value
    """
    #	Returns the Temperature of the sensor
    def getTemperature(self, mpodn, sensor):
		
        data = os.popen("snmpget -v 2c -M " + self.miblib + "-m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " sensorTemperature" + sensor)
        ret = data.read().split('\n')
		
        return ret[0].split(" ")[-2]

    #	Measures and returns the sense voltage (voltage at load)
    def getMeasurementSenseVoltage(self, mpodn, channel):
        
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " outputMeasurementSenseVoltage" + channel)
        ret = data.read().split('\n')

        return ret[0].split(" ")[-2]

    #   Measures and returns the terminal voltage (voltage just outside MPODs)
    def getMeasurementTerminalVoltage(self, mpodn, channel):

        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " outputMeasurementTerminalVoltage" + channel)
        ret = data.read().split('\n')

        return ret[0].split(" ")[-2]
	
    #   Measures and returns the current
    def getMeasurementCurrent(self, mpodn, channel):

        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " outputMeasurementCurrent" + channel)
        ret = data.read().split('\n')

        return ret[0].split(" ")[-2]

    #   Measures and returns the Temperature
    def getMeasurementTemperature(self, mpodn, channel):

        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[mpodn] + " outputMeasurementTemperature" + channel)
        ret = data.read().split('\n')

        return ret[0].split(" ")[-2]    
	
    #   Measures and returns the power output at the terminal
    def getLoadPower(self, mpodn, channel):
        mpod = mpodPsu(self.ip[mpodn])
        Power = float(mpod.getMeasurementTerminalVoltage(mpodn, channel)) * float(mpod.getMeasurementCurrent(mpodn, channel))
        return Power
	
    #   Measures and returns the power usage from all channels
    def getModulePower(self, mpodn, list):
        mpod = mpodPsu(self.ip[mpodn])
        modpow = 0
        for i in list:
            modpow += mpod.getLoadPower(mpodn,i)
        return modpow

    #   Measures and returns the status of the channel, the sense voltage, and the current for a list of channels
    def measure(self, mpodn, channels):
        Svalues = []
        Vvalues = []
        Ivalues = []
        mpod = mpodPsu(self.ip[mpodn])
        for channel in channels:
            if mpod.getStatus(mpodn, channel)[0] == "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 80 outputOn(0) ":
                Svalues += ["ON"]
            elif mpod.getStatus(mpodn, channel)[0] == "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 00 ":
                Svalues += ["OFF"]
            elif mpod.getStatus(mpodn, channel)[0] == "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 40 outputInhibit(1) ":
                Svalues += ["ILOCK"]
            else:
                Svalues += [mpod.getStatus(mpodn, channel)]
            Vvalues += [mpod.getMeasurementSenseVoltage(mpodn, channel)]
            Ivalues += [mpod.getMeasurementCurrent(mpodn, channel)]
        return Svalues,Vvalues,Ivalues

# Set commands:

    #   Sets the channel's current
    def setCurrent(self, mpodn, I, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[mpodn] + " outputCurrent" + channel + " F " + str(I))

    #   Sets the channel's voltage
    def setVoltage(self, mpodn, V, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[mpodn] + " outputVoltage" + channel + " F " + str(V))

    #   Sets the channel's maximum current
    def setMaxCurrent(self, mpodn, I, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[mpodn] + " outputSupervisionMaxCurrent" + channel + " F " + str(I))

    #   Sets the channel's maximum terminal voltage
    def setMaxVoltage(self, mpodn, V, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[mpodn] + " outputSupervisionMaxTerminalVoltage" + channel + " F " + str(V))

    #   Sets the channel's maximum sense voltage
    def setMaxSenseVoltage(self, mpodn, V, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[mpodn] + " outputSupervisionMaxSenseVoltage" + channel + " F " + str(V))

    #   Sets the channel's maximum sense voltage
    def setMinSenseVoltage(self, mpodn, V, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[mpodn] + " outputSupervisionMinSenseVoltage" + channel + " F " + str(V))

    #   Sets the channel's maximum power output
    def setMaxPower(self, mpodn):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[mpodn] + " outputSupervisionMaxPower" + channel + " F " + str(P))

    #   Sets the channel's voltage rise rate
    def setVoltageRiseRate(self, mpodn, rate, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[mpodn] + " outputVoltageRiseRate" + channel + " F " + str(rate))

    #   Sets the channel's voltage fall rate
    def setVoltageFallRate(self, mpodn, rate, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[mpodn] + " outputVoltageFallRate" + channel + " F " + str(rate))

    #   Sets the channel's current rise rate
    def setCurrentRiseRate(self, mpodn, rate, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[mpodn] + " outputCurrentRiseRate" + channel + " F " + str(rate))

    #   Sets the channel's current fall rate
    def setCurrentFallRate(self, mpodn, rate, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[mpodn] + " outputCurrentFallRate" + channel + " F " + str(rate))

    #   Sets the channel's maximum trip time for the current
    def setMaxCurrentTripTime(self, mpodn, delay, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[mpodn] + " outputTripTimeMaxCurrent" + channel + " i " + str(delay))
        
    """
    TM 21.02.2023
    """

    #   Sets the channel's maximum temperature
    def setMaxTemperature(self, mpodn, T, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c admin " + self.ip[mpodn] + " outputSupervisionMaxTemperature" + channel + " i " + str(T))
	
        """
        Predefined functions for MPOD control
        """
    	
    #	A function that will ramp up the voltage of a channel
    def ramp_up(self, mpodn, rate, V, channel):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.setVoltageRiseRate(mpodn, rate, channel)
        mpod.channelSwitch(mpodn, 1, channel)
        mpod.setVoltage(mpodn, V, channel)
        time.sleep(1)
        print(str(channel), str(mpod.getMeasurementSenseVoltage(mpodn, channel)), "V")

    #   A function that will ramp down the voltage of a channel
    def ramp_down(self, mpodn, rate, V, channel):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.setVoltageFallRate(mpodn, rate, channel)
        mpod.setVoltage(mpodn, V, channel)
        time.sleep(1)
        print(str(channel), str(mpod.getMeasurementSenseVoltage(mpodn, channel)), "V")
	

# Functions that set channels to their normal operating conditions
    def PACMAN_A_power(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.setMaxCurrent(mpodn, 3.75, ".u0")
        mpod.setCurrent(mpodn, 3.5, ".u0")
        mpod.setMaxSenseVoltage(mpodn, 24.5, ".u0")
        mpod.setMaxVoltage(mpodn, 25, ".u0")
        mpod.ramp_up(mpodn, 1000, 24.01, ".u0")

    def PACMAN_A_off(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.ramp_down(mpodn, 1000, 0, ".u0")
        mpod.channelSwitch(mpodn, 0, ".u0")

    def PACMAN_B_power(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.setMaxCurrent(mpodn, 3.75, ".u1")
        mpod.setCurrent(mpodn, 3.5, ".u1")
        mpod.setMaxSenseVoltage(mpodn, 24.5, ".u1")
        mpod.setMaxVoltage(mpodn, 25, ".u1")
        mpod.ramp_up(mpodn, 1000, 24.01, ".u1")

    def PACMAN_B_off(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.ramp_down(mpodn, 1000, 0, ".u1")
        mpod.channelSwitch(mpodn, 0, ".u1")

    def PACFAN_A_power(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.setMaxCurrent(mpodn, 0.65, ".u100")
        mpod.setCurrent(mpodn, 0.6, ".u100")
        mpod.setMaxSenseVoltage(mpodn, 13.2, ".u100")
        mpod.setMaxVoltage(mpodn, 13.2, ".u100")
        mpod.ramp_up(mpodn, 1000, 7.5, ".u100")

    def PACFAN_A_off(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.ramp_down(mpodn, 1000, 0, ".u100")
        mpod.channelSwitch(mpodn, 0, ".u100")

    def PACFAN_B_power(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.setMaxCurrent(mpodn, 0.65, ".u101")
        mpod.setCurrent(mpodn, 0.6, ".u101")
        mpod.setMaxSenseVoltage(mpodn, 13.2, ".u101")
        mpod.setMaxVoltage(mpodn, 13.2, ".u101")
        mpod.ramp_up(mpodn, 1000, 7.5, ".u101")

    def PACFAN_B_off(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.ramp_down(mpodn, 1000, 0, ".u101")
        mpod.channelSwitch(mpodn, 0, ".u101")
		
    def SC_RTD_1_power(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.setMaxCurrent(mpodn, 1.05, ".u104")
        mpod.setCurrent(mpodn, 1.0, ".u104")
        mpod.setMaxSenseVoltage(mpodn, 6, ".u104")
        mpod.setMaxVoltage(mpodn, 6, ".u104")
        mpod.ramp_up(mpodn, 1000, 5, ".u104")

    def SC_RTD_1_off(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.ramp_down(mpodn, 1000, 0, ".u104")
        mpod.channelSwitch(mpodn, 0, ".u104")
		
    def SC_RTD_2_power(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.setMaxCurrent(mpodn, 1.05, ".u106")
        mpod.setCurrent(mpodn, 1.0, ".u106")
        mpod.setMaxSenseVoltage(mpodn, 6, ".u106")
        mpod.setMaxVoltage(mpodn, 6, ".u106")
        mpod.ramp_up(mpodn, 1000, 5, ".u106")

    def SC_RTD_2_off(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.ramp_down(mpodn, 1000, 0, ".u106")
        mpod.channelSwitch(mpodn, 0, ".u106")

    def All_OFF(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        channels = [".u0", ".u1", ".u2", ".u3", ".u100", ".u101", ".u102", ".u103", ".u104", ".u105", ".u106", ".u107", ".u200", ".u201", ".u202", ".u203", ".u204", ".u205", ".u206", ".u207"]
        for i in channels:
            mpod.ramp_down(mpodn, 100, 0, i)
            mpod.channelSwitch(mpodn, 0, i)
    
    def VGA_12_pos_power(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])        
        mpod.setMaxCurrent(mpodn, 1.55, ".u200")
        mpod.setCurrent(mpodn, 1.5, ".u200")
        mpod.setMaxSenseVoltage(mpodn, 5.5, ".u200")
        mpod.setMaxVoltage(mpodn, 6, ".u200")
        mpod.ramp_up(mpodn, 100, 5, ".u200")

    def VGA_12_pos_off(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.ramp_down(mpodn, 1000, 0, ".u200")    
        mpod.channelSwitch(mpodn, 0, ".u200")

    def VGA_12_neg_power(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.setMaxCurrent(mpodn, 1.55, ".u201")
        mpod.setCurrent(mpodn, 1.5, ".u201")
        mpod.setMaxSenseVoltage(mpodn, 5.5, ".u201")
        mpod.setMaxVoltage(mpodn, 6, ".u201")
        mpod.ramp_up(mpodn, 100, 5, ".u201")

    def VGA_12_neg_off(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.ramp_down(mpodn, 1000, 0, ".u201")
        mpod.channelSwitch(mpodn,0 , ".u201")

    def VGA_34_pos_power(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.setMaxCurrent(mpodn, 1.55, ".u202")
        mpod.setCurrent(mpodn, 1.5, ".u202")
        mpod.setMaxSenseVoltage(mpodn, 5.5, ".u202")
        mpod.setMaxVoltage(mpodn, 6, ".u202")
        #mpod.ramp_up(mpodn, 1000, 4, ".u202")
        mpod.ramp_up(mpodn, 100, 5, ".u202")

    def VGA_34_pos_off(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.ramp_down(mpodn, 1000, 0, ".u202")
        mpod.channelSwitch(mpodn, 0, ".u202")

    def VGA_34_neg_power(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.setMaxCurrent(mpodn, 1.55, ".u203")
        mpod.setCurrent(mpodn, 1.5, ".u203")
        mpod.setMaxSenseVoltage(mpodn, 5.5, ".u203")
        mpod.setMaxVoltage(mpodn, 6, ".u203")
        #mpod.ramp_up(mpodn, 1000, 4, ".u203")
        mpod.ramp_up(mpodn, 100, 5, ".u203")

    def VGA_34_neg_off(self, mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.ramp_down(mpodn, 1000, 0, ".u203")
        mpod.channelSwitch(mpodn, 0, ".u203")    

    def All_ON(self,mpodn):
        mpod = mpodPsu(self.ip[mpodn])
        mpod.PACFAN_A_power(mpodn)
        mpod.PACFAN_B_power(mpodn)
        mpod.PACMAN_A_power(mpodn)
        mpod.PACMAN_B_power(mpodn)
        mpod.SC_RTD_1_power(mpodn)
        mpod.SC_RTD_2_power(mpodn)
        mpod.VGA_12_pos_power(mpodn)
        mpod.VGA_12_neg_power(mpodn)
        mpod.VGA_34_pos_power(mpodn)
        mpod.VGA_34_neg_power(mpodn) 	

    """
    RV 07.18.2023
    """

    def JSON_setup(self, measurement, module, status, voltage, current):
        '''
        Inputs:         - Measurement (i.e. light)
                        - Module (i.e. VGA_12_POS)
                        - Status (i.e. OFF)
                        - Fields (Voltage & current)

        Outputs:        - JSON file ready to be added to InfluxDB

        Description:    Provides new timestamp ready to be added to InfluxDB
        '''
        json_payload = []
        data = {
            # Table name
            "measurement" : measurement, 
            # Organization tags
            "tags" : { 
                "module" : module,
                "status" : status
            },
            # Time stamp
            "time" : datetime.now().strftime('%Y%m%d %H:%M:%S'), 
            # Data fields
            "fields" : { 
                "voltage" : voltage,
                "current" : current
            }
        }
        json_payload.append(data)
        return json_payload

    def INFLUX_write(self, powering, modules, data, mpod, client):
        '''
        Inputs:         - Powering (i.e. light)
                        - Module (i.e. VGA_12_POS)
                        - Data (MPOD measurement array)
                        - MPOD (MPOD instance)
                        - Client (InfluxDB client)

        Description:    Record timestamp on InfluxDB
        '''
        data = np.array(data)
        for module_number in range(0,data.shape[1]):
            data_column = data[:,module_number]
            client.write_points(mpod.JSON_setup(
                measurement = powering,
                module = modules[module_number],
                status = data_column[0],
                voltage = data_column[1],
                current = data_column[2]
            ))
    
    def CONTINUOUS_monitoring(self, powering, modules, mpod, mpodn, channels, client):
        '''
        Inputs:         - Powering (i.e. light)
                        - Module (i.e. VGA_12_POS)
                        - MPOD (MPOD instance)
                        - MPODn (MPOD number selected)
                        - Channels (List of channels)
                        - Client (InfluxDB client)

        Description:    Continuously record timestamp on InfluxDB
        '''
        try:
            print('~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#')
            print("Continuous DAQ Activated")
            print("Taking data in real time")
            print('~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#')
            while True:
                data = mpod.measure(mpodn,channels)
                mpod.INFLUX_write(powering,modules,data,mpod,client)
                time.sleep(2)
        except KeyboardInterrupt:
            print('~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#')
            print("Continuous DAQ Terminated")
            print('~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#')
            raise SystemExit
    