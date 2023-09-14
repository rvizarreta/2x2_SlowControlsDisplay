from pysnmp.hlapi import *
import os
import time 

class vmePsu():
    
    def __init__(self,ip = ['192.168.196.100'], miblib='./mibs/'):
        self.ip = ['192.168.196.100']
        self.miblib = miblib 

# Power switches

    def vmeSwitch(self, vmen, switch):
        os.popen("snmpset -v 2c -M " + str(self.miblib) + " -m +WIENER-CRATE-MIB -c guru " + str(self.ip[vmen]) + " sysMainSwitch.0 i " + str(switch))
        #os.popen("snmpset -v 2c -M ./mibs -m +WIENER-CRATE-MIB -c guru " + self.ip[0] + " sysMainSwitch.0 i " + str(switch))

    #	Individual Channel Switch
    #	Valid channels include ".u0", ".u1", ".u3", ".u5"
    def channelSwitch(self, vmen, switch, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[vmen] + " outputSwitch" + channel + " i " + str(switch))

    def walk(self, vmen):
        os.popen("snmpwalk -v 2c -M " + self.miblib +" -m +WIENER-CRATE-MIB -c public " + self.ip[vmen] + " [OID]")	
# Get commands:

    #	Retruns the status of the output channel
    def getStatus(self, vmen, channel):

        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[vmen] + " outputStatus" + channel)
        ret = data.read().split('\n')

        return ret

    #	Returns the voltage that the channel was set to
    def getVoltage(self, vmen, channel):

        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[vmen] + " outputVoltage" + channel)
        ret = data.read().split('\n')

        return ret[0].split(" ")[-2]

    #	Returns the current that the channel was set to
    def getCurrent(self, vmen, channel):

        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[vmen] + " outputCurrent" + channel)
        ret = data.read().split('\n')

        return ret[0].split(" ")[-2]

    def behavior(self, vmen, channel):
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[vmen] + " outputSupervisionBehavior" +channel)
        ret = data.read().split('\n')

        return ret
        
    """
    TM 17.02.2023
    get(current/voltage) gets the set value
    getMeasurement______(current/voltage) gets real value
    """
    #	Returns the Temperature of the sensor
    def getTemperature(self, vmen, sensor):
		
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[vmen] + " sensorTemperature" + sensor)
        ret = data.read().split('\n')
		
        return ret[0].split(" ")[-2]

    #	Measures and returns the sense voltage (voltage at load)
    def getMeasurementSenseVoltage(self, vmen, channel):
        
        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[vmen] + " outputMeasurementSenseVoltage" + channel)
        ret = data.read().split('\n')

        return ret[0].split(" ")[-2]

    #   Measures and returns the terminal voltage (voltage just outside MPODs)
    def getMeasurementTerminalVoltage(self, vmen, channel):

        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[vmen] + " outputMeasurementTerminalVoltage" + channel)
        ret = data.read().split('\n')

        return ret[0].split(" ")[-2]
	
    #   Measures and returns the current
    def getMeasurementCurrent(self, vmen, channel):

        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[vmen] + " outputMeasurementCurrent" + channel)
        ret = data.read().split('\n')

        return ret[0].split(" ")[-2]

    #   Measures and returns the Temperature
    def getMeasurementTemperature(self, vmen, channel):

        data = os.popen("snmpget -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c public " + self.ip[vmen] + " outputMeasurementTemperature" + channel)
        ret = data.read().split('\n')

        return ret[0].split(" ")[-2]    
	
    #   Measures and returns the power output at the terminal
    def getLoadPower(self, vmen, channel):
        mpod = mpodPsu(self.ip[vmen])
        Power = float(mpod.getMeasurementTerminalVoltage(vmen, channel)) * float(mpod.getMeasurementCurrent(vmen, channel))
        return Power
	
    #   Measures and returns the power usage from all channels
    def getModulePower(self, vmen, list):
        mpod = mpodPsu(self.ip[vmen])
        modpow = 0
        for i in list:
            modpow += mpod.getLoadPower(vmen,i)
        return modpow

    #   Measures and returns the status of the channel, the sense voltage, and the current for a list of channels
    def measure(self, vmen, channels):
        Svalues = []
        Vvalues = []
        Ivalues = []
        mpod = mpodPsu(self.ip[vmen])
        for channel in channels:
            if mpod.getStatus(vmen, channel)[0] == "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 80 outputOn(0) ":
                Svalues += ["ON"]
            elif mpod.getStatus(vmen, channel)[0] == "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 00 ":
                Svalues += ["OFF"]
            elif mpod.getStatus(vmen, channel)[0] == "WIENER-CRATE-MIB::outputStatus"+channel+" = BITS: 40 outputInhibit(1) ":
                Svalues += ["ILOCK"]
            else:
                Svalues += [mpod.getStatus(vmen, channel)]
            Vvalues += [mpod.getMeasurementSenseVoltage(vmen, channel)]
            Ivalues += [mpod.getMeasurementCurrent(vmen, channel)]
        return Svalues,Vvalues,Ivalues

# Set commands:

    #   Sets the channel's current
    def setCurrent(self, vmen, I, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[vmen] + " outputCurrent" + channel + " F " + str(I))

    #   Sets the channel's voltage
    def setVoltage(self, vmen, V, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[vmen] + " outputVoltage" + channel + " F " + str(V))

    #   Sets the channel's maximum current
    def setMaxCurrent(self, vmen, I, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[vmen] + " outputSupervisionMaxCurrent" + channel + " F " + str(I))

    #   Sets the channel's maximum terminal voltage
    def setMaxVoltage(self, vmen, V, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[vmen] + " outputSupervisionMaxTerminalVoltage" + channel + " F " + str(V))

    #   Sets the channel's maximum sense voltage
    def setMaxSenseVoltage(self, vmen, V, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[vmen] + " outputSupervisionMaxSenseVoltage" + channel + " F " + str(V))

    #   Sets the channel's maximum power output
    def setMaxPower(self, vmen):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[vmen] + " outputSupervisionMaxPower" + channel + " F " + str(P))

    #   Sets the channel's voltage rise rate
    def setVoltageRiseRate(self, vmen, rate, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[vmen] + " outputVoltageRiseRate" + channel + " F " + str(rate))

    #   Sets the channel's voltage fall rate
    def setVoltageFallRate(self, vmen, rate, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[vmen] + " outputVoltageFallRate" + channel + " F " + str(rate))

    #   Sets the channel's current rise rate
    def setCurrentRiseRate(self, vmen, rate, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[vmen] + " outputCurrentRiseRate" + channel + " F " + str(rate))

    #   Sets the channel's current fall rate
    def setCurrentFallRate(self, vmen, rate, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[vmen] + " outputCurrentFallRate" + channel + " F " + str(rate))

    #   Sets the channel's maximum trip time for the current
    def setMaxCurrentTripTime(self, vmen, delay, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c guru " + self.ip[vmen] + " outputTripTimeMaxCurrent" + channel + " i " + str(delay))
        
    """
    TM 21.02.2023
    """

    #   Sets the channel's maximum temperature
    def setMaxTemperature(self, vmen, T, channel):
        os.popen("snmpset -v 2c -M " + self.miblib + " -m +WIENER-CRATE-MIB -c admin " + self.ip[vmen] + " outputSupervisionMaxTemperature" + channel + " i " + str(T))
	
        """
        Predefined functions for MPOD control
        """
    	
    #	A function that will ramp up the voltage of a channel
    def ramp_up(self, vmen, rate, V, channel):
        mpod = mpodPsu(self.ip[vmen])
        mpod.setVoltageRiseRate(vmen, rate, channel)
        mpod.channelSwitch(vmen, 1, channel)
        mpod.setVoltage(vmen, V, channel)
        time.sleep(1)
        print(str(channel), str(mpod.getMeasurementSenseVoltage(vmen, channel)), "V")

    #   A function that will ramp down the voltage of a channel
    def ramp_down(self, vmen, rate, V, channel):
        mpod = mpodPsu(self.ip[vmen])
        mpod.setVoltageFallRate(vmen, rate, channel)
        mpod.setVoltage(vmen, V, channel)
        time.sleep(1)
        print(str(channel), str(mpod.getMeasurementSenseVoltage(vmen, channel)), "V")
