import time
import subprocess
from configparser import ConfigParser
from vme_library import vmePsu
import influxdb as ifd

"""
sudo apt-get install snmp-mibs-downloader
sudo apt-get install snmpd
sudo apt-get install snmp
"""

if __name__ == "__main__":

	# placeholder config file to define global variables
	conf = ConfigParser()
	conf.read("./config.ini") # where is this file — ask livio

	# define variables
	db = conf["DATABASE"]
	meta = conf["METADATA"]
	para = conf["PARAMETERS"]

	# initialize module #
	meta["MODULE"]

	# initialize MPOD class
	
	vme = vmePsu(['192.168.196.100'])

	def validate_mpodn(TTIn):
		if TTIn == 0 or TTIn == 1:
			return TTIn, True
		else:
		        return TTIn, False
	
	# Validates the user input for controlling on and off settings
	def ONOFF_is_valid(string):
		if string == "on" or string == "On":
			string = "ON"
		elif string == "Off" or string == "off":
			string = "OFF"
		if string == "ON" or string == "OFF":
			return string, True
		else:
			print("Invalid input, valid inputs include ON and OFF")
			return string, False

	ONOFF = input("Are you turning on or off the power? ")
	validation = ONOFF_is_valid(ONOFF)
	ONOFF = validation[0]
	valid = validation[1]
	while valid == False:
		ONOFF = input("Are you turning ON or OFF the power? ")
		validation = ONOFF_is_valid(ONOFF)
		ONOFF = validation[0]
		valid = validation[1]

	if ONOFF == "ON":
		vme.vmeSwitch(0,1)
		print("The VME crate is on")
	elif ONOFF == "OFF":
		vme.vmeSwitch(0,0)
		print("The VME crate is off")
	
	print(vme.getTemperature(0, ".temp1"))
	"""
	mpodn = int(input("What MPOD would you like to control (0,1) "))
	while validate_mpodn(mpodn)[1] == False:
		print(validate_mpodn(mpodn))
		mpodn = int(input("What MPOD would you like to control (0,1) "))
 	
	vme.vmeSwitch(mpodn,0)
	"""
	"""
	# List of various channels and names 
	channels = [".u0", ".u1", ".u2", ".u3", ".u100", ".u101", ".u102", ".u103", ".u104", ".u105", ".u106", ".u107", ".u200", ".u201", ".u202", ".u203", ".u204", ".u205", ".u206", ".u207"]
	light_channels = [".u200",".u201",".u202",".u203"]
	light_names = ["VGA_12_pos","VGA_12_neg","VGA_34_pos","VGA_34_neg"]
	
	charge_channels = [".u0",".u1",".u100",".u101"]
	charge_names = ["PACMAN_A","PACMAN_B","PACFAN_A","PACFAN_B"]

	RTD_channels = [".u104",".u106"]
	RTD_names = ["RTD_1","RTD_2"]	

	charge_n_light_channels = charge_channels + light_channels + RTD_channels
	charge_n_light_names = charge_names + light_names + RTD_names
		
	# Validates the user input for controlling on and off settings
	def ONOFF_is_valid(string):
		if string == "on" or string == "On":
			string = "ON"
		elif string == "Off" or string == "off":
			string = "OFF"
		if string == "ON" or string == "OFF":
			return string, True
		else:
			print("Invalid input, valid inputs include ON and OFF")
			return string, False
	# Validates the user input for controlling the measurement or setting procedures
	def mos_is_valid(string):
		if string == "view" or string == "VIEW" or string == "v":
			string = "View"
		elif string == "CONFIGURE" or string == "configure" or string == "c":
			string = "Configure"
		if string == "Configure" or string == "View":
			return string,True
		else:
			print("Invalid input, valid inputs include View and Configure")
			return string, False
	
	# Validates the user input for controlling what systems to turn on with MPODs
	def CONTROL_is_valid(string):
		if string == "charge" or string == "CHARGE" or string == "c" or string == "C":
			string = "Charge"
		elif string == "light" or string == "LIGHT" or string == "l" or string == "L":
			string = "Light"
		elif string == "RTD" or string == "SC" or string == "sc" or string == "rtd":
			string = "Rtd"
		elif string == "ALL" or string == "all" or string == "a" or string == "A":
			string = "All"
		if string == "Charge" or string == "Light" or string == "Rtd" or string == "All":
			return string, True
		else:
			print("Invalid input, valid inputs are Charge, Light, Rtd, or All")
			return string, False
	# Gathers input regarding what systems to power
	powering = input("What would you like to control (Charge,Light,Rtd,All)? ")
	validation = CONTROL_is_valid(powering)
	powering = validation[0]
	valid = validation[1]
	while valid == False:
		powering = input("What would you like to control (Charge,Light,Rtd,All)? ")
		validation = CONTROL_is_valid(powering)
		powering = validation[0]
		valid = validation[1]
	
	# Gathers input regarding setting or measureing
	measureorset = input("Would you like to View or Configure channels? ")
	validation = mos_is_valid(measureorset)
	measureorset = validation[0]
	valid = validation[1]
	while valid == False:	
		measureorset = input("Would you like to View or Configure channels? ")
		validation = mos_is_valid(measureorset)
		measureorset = validation[0]
		valid = validation[1]
	
	# If the user wants to set power supplies it gets an on/off input
	if measureorset == "Configure":
		ONOFF = input("Are you turning on or off the power? ")
		validation = ONOFF_is_valid(ONOFF)
		ONOFF = validation[0]
		valid = validation[1]
		while valid == False:
			ONOFF = input("Are you turning ON or OFF the power? ")
			validation = ONOFF_is_valid(ONOFF)
			ONOFF = validation[0]
			valid = validation[1]

	# Controls the light setting
	if powering == "Light":
		# Turns on/off
		if measureorset == "Configure":
			if ONOFF == "ON":
				vme.VGA_12_pos_power(mpodn)
				vme.VGA_12_neg_power(mpodn)
				vme.VGA_34_pos_power(mpodn)
				vme.VGA_34_neg_power(mpodn)
			elif ONOFF == "OFF":
				vme.VGA_12_pos_off(mpodn)
				vme.VGA_12_neg_off(mpodn)
				vme.VGA_34_pos_off(mpodn)
				vme.VGA_34_neg_off(mpodn)
			turn_off = input("Would you like to power off the MPOD crate? ")
			if turn_off == "y" or "Y" or "yes" or "Yes" or "YES":
				vme.mpodSwitch(mpodn,0)
				print("MPOD is now off")
			else:
				print("MPOD is stil on")

		# Measures
		if measureorset == "View":
			data = vme.measure(mpodn,light_channels)
			print(light_names[0], '\t', light_names[1], '\t', light_names[2], '\t', light_names[3])
			print("   ",data[0][0], '    \t    ', data[0][1], '    \t    ', data[0][2], '    \t    ', data[0][3], '')
			print(data[1][0], 'V \t', data[1][1], 'V \t', data[1][2], 'V \t', data[1][3], 'V')
			print(data[2][0], 'I \t', data[2][1], 'I \t', data[2][2], 'I \t', data[2][3], 'I')
	
	# Controls light
	elif powering == "Charge":
		# Turns on/off
		if measureorset == "Configure":
			if ONOFF == "ON":
				vme.PACFAN_A_power(mpodn)
				vme.PACFAN_B_power(mpodn)
				print("PACFANs are powered on")
				time.sleep(5)
				vme.PACMAN_A_power(mpodn)
				vme.PACMAN_B_power(mpodn)
				print("PACMANs are powered on")
			elif ONOFF == "OFF":
				vme.PACMAN_A_off(mpodn)
				vme.PACMAN_B_off(mpodn)
				print("PACMANs are powered off")
				time.sleep(5)
				vme.PACFAN_A_off(mpodn)
				vme.PACFAN_B_off(mpodn)
				print("PACFANs are powered off")
			turn_off = input("Would you like to power off the MPOD crate? ")
			if turn_off == "y" or "Y" or "yes" or "Yes" or "YES":
				vme.mpodSwitch(mpodn,0)
				print("MPOD is now off")
			else:
				print("MPOD is stil on")

		# Measures and displays the channel, the status, the voltage, and the current
		if measureorset == "View":
                        data = vme.measure(mpodn,charge_channels)
                        print(charge_names[0], '\t', charge_names[1], '\t', charge_names[2], '\t', charge_names[3])
                        print("   ",data[0][0], '    \t    ', data[0][1], '    \t    ', data[0][2], '    \t    ', data[0][3], '')
                        print(data[1][0], 'V \t', data[1][1], 'V \t', data[1][2], 'V \t', data[1][3], 'V')
                        print(data[2][0], 'I \t', data[2][1], 'I \t', data[2][2], 'I \t', data[2][3], 'I')
	
	# Controls RTDs
	elif powering == "Rtd":
		# Turns on/off
		if measureorset == "Configure":
			if ONOFF == "ON":
				vme.SC_RTD_1_power(mpodn)
				vme.SC_RTD_2_power(mpodn)
				print("RTDs are powered on")
			elif ONOFF == "OFF":
				vme.SC_RTD_1_off(mpodn)
				vme.SC_RTD_2_off(mpodn)
				print("RTDs are powered off")
			turn_off = input("Would you like to power off the MPOD crate? ")
			if turn_off == "y" or "Y" or "yes" or "Yes" or "YES":
				vme.vmeSwitch(mpodn,0)
				print("MPOD is now off")
			else:
				print("MPOD is stil on")

		# Measures and displays the channel, the status, the voltage, and the current
		if measureorset == "View":
			data = vme.measure(mpodn,RTD_channels)
			print(RTD_names[0], '\t', RTD_names[1])
			print("   ",data[0][0], '    \t    ', data[0][1])
			print(data[1][0], 'V \t', data[1][1], 'V \t')
			print(data[2][0], 'I \t', data[2][1], 'I \t')

	# Controls All channels
	elif powering == "All":
		# Turns on/off
		if measureorset == "Configure":
			if ONOFF == "ON":
				vme.All_ON(mpodn)
			elif ONOFF == "OFF":
				vme.All_OFF(mpodn)
				turn_off = input("Would you like to power off the MPOD crate? ")
				if turn_off == "y" or "Y" or "yes" or "Yes" or "YES":
					vme.mpodSwitch(mpodn,0)
					print("MPOD is now off")
				else:
					print("MPOD is stil on")
		# Measures and displays the channel, the status, the voltage, and the current
		if measureorset == "View":
                        data = vme.measure(mpodn,charge_n_light_channels)
                        print(charge_n_light_names[0], '\t ', charge_n_light_names[1], '\t ', charge_n_light_names[2], '\t ', charge_n_light_names[3],'\t',charge_n_light_names[4], '\t', charge_n_light_names[5], '\t', charge_n_light_names[6], '\t', charge_n_light_names[7])
                        print("   ",data[0][0], '    \t    ', data[0][1], '    \t    ', data[0][2], '    \t    ', data[0][3], "   \t    ",data[0][4], '    \t    ', data[0][5], '    \t    ', data[0][6], '    \t    ', data[0][7],)
                        print(data[1][0], 'V \t', data[1][1], 'V \t', data[1][2], 'V \t', data[1][3], 'V \t',data[1][4], 'V \t', data[1][5], 'V \t', data[1][6], 'V \t', data[1][7], 'V')
                        print(data[2][0], 'I \t', data[2][1], 'I \t', data[2][2], 'I \t', data[2][3], 'I \t',data[2][4], 'I \t', data[2][5], 'I \t', data[2][6], 'I \t', data[2][7], 'I')
"""
