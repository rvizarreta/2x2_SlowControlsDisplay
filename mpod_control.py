import time
import subprocess
from configparser import ConfigParser
from mpod_library import mpodPsu
#import influxdb as ifd
import sys
# InfluxDB required packages
from influxdb import InfluxDBClient
from datetime import datetime

"""
sudo apt-get install snmp-mibs-downloader
sudo apt-get install snmpd
sudo apt-get install snmp
"""

if __name__ == "__main__":
	try:
		tutorial = str(sys.argv[1])
		if tutorial == "-n":
			tutorial = True
		else:
			tutorial = False
	except:
                tutorial = False
	if tutorial == False:
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
		mpod = mpodPsu(['192.168.196.6','192.168.196.7'])

		######################################################
		"""
		RV 07.18.2023
		"""
		# Initialize InfluxDB client
		client = InfluxDBClient('localhost', 8086, 'MPODs')
		client.create_database('MPODs')
		client.switch_database('MPODs')
		######################################################
	
		def validate_mpodn(TTIn):
			if TTIn == 0 or TTIn == 1:
				return TTIn, True
			else:
			        return TTIn, False
		print('~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#')
		mpodn = int(input("What MPOD would you like to control? (insert number only) \n - MPOD 0 \n - MPOD 1 \n Answer:  "))
		while validate_mpodn(mpodn)[1] == False:
			print(validate_mpodn(mpodn))
			mpodn = int(input("What MPOD would you like to control (0,1) "))
 	
		mpod.mpodSwitch(mpodn,1)

		# At this point we write the log file
		mpod.write_log()


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
			'''
			if string == "view" or string == "VIEW" or string == "v":
				string = "View"
			elif string == "CONFIGURE" or string == "configure" or string == "c":
				string = "Configure"
			if string == "Configure" or string == "View":
				return string,True
			else:
				print("Invalid input, valid inputs include View and Configure")
				return string, False
			'''
			######################################################
			"""
			RV 07.18.2023
			"""
			actions = {
				'monitor': 'Monitor',
				'view' : 'View',
				'configure' : 'Configure'
			}
			normalized_input = string.lower()
			first_letters = [key[0].lower() for key in actions] 	
			if normalized_input in actions:
				string = actions[normalized_input] 
				return string, True
			elif normalized_input[0] in first_letters:
				index = first_letters.index(normalized_input[0])
				string = list(actions.items())[index][1]
				return string, True
			else:
				print("Invalid input.")
				return string, False
			######################################################

	
		# Validates the user input for controlling what systems to turn on with MPODs
		def CONTROL_is_valid(string):
			'''
			if string == "charge" or string == "CHARGE" or string == "c" or string == "C":
				string = "Charge"
			elif string == "light" or string == "LIGHT" or string == "l" or string == "L":
				string = "Light"
			elif string == "RTD" or string == "SC" or string == "sc" or string == "rtd" or string == "r" or string == "R":
				string = "Rtd"
			elif string == "ALL" or string == "all" or string == "a" or string == "A":
				string = "All"
			if string == "Charge" or string == "Light" or string == "Rtd" or string == "All":
				return string, True
			else:
				print("Invalid input, valid inputs are Charge, Light, Rtd, or All")
				return string, False
			'''
			######################################################
			"""
			RV 07.18.2023
			"""
			actions = {
				'charge': 'Charge',
				'light' : 'Light',
				'rtd' : 'Rtd',
				'all' : 'All'
			}
			normalized_input = string.lower()
			first_letters = [key[0].lower() for key in actions] 	
			if normalized_input in actions:
				string = actions[normalized_input] 
				return string, True
			elif normalized_input[0] in first_letters:
				index = first_letters.index(normalized_input[0])
				string = list(actions.items())[index][1]
				return string, True
			else:
				print("Invalid input.")
				return string, False
			######################################################
			
		# Gathers input regarding what systems to power
		print('~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#')
		#powering = input("What would you like to control (Charge,Light,Rtd,All)? ")
		powering = input("What would you like to control? \n - Charge \n - Light \n - Rtd \n - All \n Answer: ")
		validation = CONTROL_is_valid(powering)
		powering = validation[0]
		valid = validation[1]
		while valid == False:
			print('~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#')
			#powering = input("What would you like to control (Charge,Light,Rtd,All)? ")
			powering = input("What would you like to control? \n - Charge \n - Light \n - Rtd \n - All \n Answer: ")
			validation = CONTROL_is_valid(powering)
			powering = validation[0]
			valid = validation[1]
		
		# Gathers input regarding setting or measureing
		print('~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#')
		measureorset = input("What would you like to do? \n - Monitor \n - View \n - Configure \n Answer: ")
		validation = mos_is_valid(measureorset)
		measureorset = validation[0]
		valid = validation[1]
		while valid == False:	
			measureorset = input("What would you like to do? \n - Monitor \n - View \n - Configure \n Answer: ")
			validation = mos_is_valid(measureorset)
			measureorset = validation[0]
			valid = validation[1]
		
		# If the user wants to set power supplies it gets an on/off input
		if measureorset == "Configure":
			print('~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#')
			ONOFF = input("Are you turning ON or OFF the power? \n Answer: ")
			validation = ONOFF_is_valid(ONOFF)
			ONOFF = validation[0]
			valid = validation[1]
			while valid == False:
				print('~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#~#')
				ONOFF = input("Are you turning ON or OFF the power? \n Answer: ")
				validation = ONOFF_is_valid(ONOFF)
				ONOFF = validation[0]
				valid = validation[1]

		# Controls the light setting
		if powering == "Light":
			# Turns on/off
			if measureorset == "Configure":
				if ONOFF == "ON":
					mpod.VGA_12_pos_power(mpodn)
					mpod.VGA_12_neg_power(mpodn)
					mpod.VGA_34_pos_power(mpodn)
					mpod.VGA_34_neg_power(mpodn)
					mpod.write_log()
				elif ONOFF == "OFF":
					mpod.VGA_12_pos_off(mpodn)
					mpod.VGA_12_neg_off(mpodn)
					mpod.VGA_34_pos_off(mpodn)
					mpod.VGA_34_neg_off(mpodn)
					mpod.write_log()
				turn_off = input("Would you like to power OFF the MPOD crate? \n Answer: ")
				if turn_off == "y" or "Y" or "yes" or "Yes" or "YES":
					mpod.mpodSwitch(mpodn,0)
					print("MPOD is now OFF")
				else:
					print("MPOD is stil ON")
	
			# Measures
			if measureorset == "View":
				data = mpod.measure(mpodn,light_channels)
				print(light_names[0], '\t', light_names[1], '\t', light_names[2], '\t', light_names[3])
				print("   ",data[0][0], '    \t    ', data[0][1], '    \t    ', data[0][2], '    \t    ', data[0][3], '')
				print(data[1][0], 'V \t', data[1][1], 'V \t', data[1][2], 'V \t', data[1][3], 'V')
				print(data[2][0], 'I \t', data[2][1], 'I \t', data[2][2], 'I \t', data[2][3], 'I')
				mpod.write_log()

				######################################################
				"""
				RV 07.18.2023
				"""
				mpod.INFLUX_write(powering,light_names,data,mpod,client)
				######################################################

			######################################################
			"""
			RV 07.18.2023
			"""
			# Monitor
			if measureorset == "Monitor":
				mpod.CONTINUOUS_monitoring(powering, light_names, mpod, mpodn, light_channels, client)
			######################################################

		# Controls light
		elif powering == "Charge":
			# Turns on/off
			if measureorset == "Configure":
				if ONOFF == "ON":
					mpod.PACFAN_A_power(mpodn)
					mpod.PACFAN_B_power(mpodn)
					print("PACFANs are powered on")
					time.sleep(5)
					mpod.PACMAN_A_power(mpodn)
					mpod.PACMAN_B_power(mpodn)
					print("PACMANs are powered on")
					mpod.write_log()
				elif ONOFF == "OFF":
					mpod.PACMAN_A_off(mpodn)
					mpod.PACMAN_B_off(mpodn)
					print("PACMANs are powered off")
					time.sleep(5)
					mpod.PACFAN_A_off(mpodn)
					mpod.PACFAN_B_off(mpodn)
					mpod.write_log()
					print("PACFANs are powered off")
				turn_off = input("Would you like to power OFF the MPOD crate? \n Answer: ")
				if turn_off == "y" or "Y" or "yes" or "Yes" or "YES":
					mpod.mpodSwitch(mpodn,0)
					print("MPOD is now off")
				else:
					print("MPOD is stil on")
	
			# Measures and displays the channel, the status, the voltage, and the current
			if measureorset == "View":
				data = mpod.measure(mpodn,charge_channels)
				print(charge_names[0], '\t', charge_names[1], '\t', charge_names[2], '\t', charge_names[3])
				print("   ",data[0][0], '    \t    ', data[0][1], '    \t    ', data[0][2], '    \t    ', data[0][3], '')
				print(data[1][0], 'V \t', data[1][1], 'V \t', data[1][2], 'V \t', data[1][3], 'V')
				print(data[2][0], 'I \t', data[2][1], 'I \t', data[2][2], 'I \t', data[2][3], 'I')
				mpod.write_log()

				######################################################
				"""
				RV 07.18.2023
				"""
				mpod.INFLUX_write(powering,charge_names,data,mpod,client)
				######################################################

			######################################################
			"""
			RV 07.18.2023
			"""
			# Monitor
			if measureorset == "Monitor":
				mpod.CONTINUOUS_monitoring(powering, charge_names, mpod, mpodn, charge_channels, client)
			######################################################

		# Controls RTDs
		elif powering == "Rtd":
			# Turns on/off
			if measureorset == "Configure":
				if ONOFF == "ON":
					mpod.SC_RTD_1_power(mpodn)
					mpod.SC_RTD_2_power(mpodn)
					print("RTDs are powered ON")
					mpod.write_log()
				elif ONOFF == "OFF":
					mpod.SC_RTD_1_off(mpodn)
					mpod.SC_RTD_2_off(mpodn)
					print("RTDs are powered OFF")
					mpod.write_log()
				turn_off = input("Would you like to power OFF the MPOD crate? \n Answer: ")
				if turn_off == "y" or "Y" or "yes" or "Yes" or "YES":
					mpod.mpodSwitch(mpodn,0)
					print("MPOD is now OFF")
				else:
					print("MPOD is stil ON")
	
			# Measures and displays the channel, the status, the voltage, and the current
			if measureorset == "View":
				data = mpod.measure(mpodn,RTD_channels)
				print(RTD_names[0], '\t', RTD_names[1])
				print("   ",data[0][0], '    \t    ', data[0][1])
				print(data[1][0], 'V \t', data[1][1], 'V \t')
				print(data[2][0], 'I \t', data[2][1], 'I \t')
				mpod.write_log()

				######################################################
				"""
				RV 07.18.2023
				"""
				mpod.INFLUX_write(powering,RTD_names,data,mpod,client)
				######################################################

			######################################################
			"""
			RV 07.18.2023
			"""
			# Monitor
			if measureorset == "Monitor":
				mpod.CONTINUOUS_monitoring(powering, RTD_names, mpod, mpodn, RTD_channels, client)
			######################################################

				
		# Controls All channels
		elif powering == "All":
			# Turns on/off
			if measureorset == "Configure":
				if ONOFF == "ON":
					mpod.All_ON(mpodn)
					mpod.write_log()
				elif ONOFF == "OFF":
					mpod.All_OFF(mpodn)
					mpod.write_log()
					turn_off = input("Would you like to power off the MPOD crate? ")
					if turn_off == "y" or "Y" or "yes" or "Yes" or "YES":
						mpod.mpodSwitch(mpodn,0)
						print("MPOD is now off")
					else:
						print("MPOD is stil on")
			# Measures and displays the channel, the status, the voltage, and the current
			if measureorset == "View":
				data = mpod.measure(mpodn,charge_n_light_channels)
				print(charge_n_light_names[0], '\t ', charge_n_light_names[1], '\t ', charge_n_light_names[2], '\t ', charge_n_light_names[3],'\t',charge_n_light_names[4], '\t', charge_n_light_names[5], '\t', charge_n_light_names[6], '\t', charge_n_light_names[7])
				print("   ",data[0][0], '    \t    ', data[0][1], '    \t    ', data[0][2], '    \t    ', data[0][3], "   \t    ",data[0][4], '    \t    ', data[0][5], '    \t    ', data[0][6], '    \t    ', data[0][7],)
				print(data[1][0], 'V \t', data[1][1], 'V \t', data[1][2], 'V \t', data[1][3], 'V \t',data[1][4], 'V \t', data[1][5], 'V \t', data[1][6], 'V \t', data[1][7], 'V')
				print(data[2][0], 'I \t', data[2][1], 'I \t', data[2][2], 'I \t', data[2][3], 'I \t',data[2][4], 'I \t', data[2][5], 'I \t', data[2][6], 'I \t', data[2][7], 'I')
				mpod.write_log()

				######################################################
				"""
				RV 07.18.2023
				"""
				mpod.INFLUX_write(powering,charge_n_light_names,data,mpod,client)
				######################################################

			######################################################
			"""
			RV 07.18.2023
			"""
			# Monitor
			if measureorset == "Monitor":
				mpod.CONTINUOUS_monitoring(powering, charge_n_light_names, mpod, mpodn, charge_n_light_channels, client)
			######################################################
				
	else:
		print('\n')
		print("Your first prompt will be to enter the number of the MPOD")
		print("This will tell the program which IP address to use")
		print("0 corresponds to the MPOD controlling modules 0 and 1")
		print("1 corresponds to the MPOD controlling modules 2 and 3")
		print("Any inputs besides 0 and 1 will be rejected")
		print("\n")
		dummy = input("Press Enter to continue")

		print("\n")
		print("The second prompt will be to enter the system you want to use")
		print("Your options are Charge, Light, Rtd, and All")
		print("I have included other strings to make your life easier like: c, l, r")
		print("\n")
		dummy = input("Press Enter to continue")

		print("\n")
		print("Now that you have selected the system, it is time to determine what you want to do")
		print("Either you can configure or view")
		print("CONFIGURE")
		print("\tWith the configure option, you can turn on or off the listed below")
		print("\tCharge: PACMANs & Fans \n \tLight: VGAs \n \tRTDs: RTD bias \n \tAll: all of the systems at once")
		print("\tWhen turned on they will be set according the Slow Controls Settings spreadsheet (DocDB 28372)")
		print("\tIf there a channel is misconfigured consult the manuals (DocDB 28372) or contact Tom (thmurphy@syr.edu)")
		print("VIEW")
		print("\tThis option will spit out the channel names and some measurments")
		print("\tStatus of channel, Sense Voltage, and Current")
		print("\n")
		dummy = input("Press Enter to continue")
		
		print("\n")
		print("For more details about each of the functions see mpod_library.py")
		print("For a detailed description of the snmp commands use 'wtf_is' command")
		print("The command is already setup in the 'test.py' file")
		print('\n')
