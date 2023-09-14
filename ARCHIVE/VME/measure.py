import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from random import randrange
import time
import subprocess
from configparser import ConfigParser
from mpod_library import mpodPsu
import influxdb as ifd
from datetime import datetime
import numpy as np
import time 

channels = [".u0", ".u1", ".u100", ".u101", ".u104", ".u106", ".u200", ".u201",".u202",".u203"]
save = True

def mpodviewer(channells):

	duration = 5
	
	now = datetime.now()
	
	fig, ((SenseV,TerminalV),(LoadP,ModP),(CurrentA,TempC)) = plt.subplots(3,2)
	fig.set_figheight(10)
	fig.set_figwidth(20)

	"""
	Sense voltage is what we readout
	Apply some corrections to get Terminal 
	"""

	time_SV = [0]
	SV = [[0] for i in range(len(channells))]
	time_TV = [0]
	TV = [[0] for i in range(len(channells))]

	time_LP = [0]
	LP = [[0] for i in range(len(channells))]
	time_MP = [0]
	MP = [[0] for i in range(len(channells))]

	time_CA = [0]
	CA = [[0] for i in range(len(channells))]
	time_TC = [0]
	TC = [[0] for i in range(len(channells))]

	ln_SV = [[0] for i in range(len(channells))]
	ln_TV = [[0] for i in range(len(channells))]
	ln_LP = [[0] for i in range(len(channells))]
	ln_MP = [[0] for i in range(len(channells))]
	ln_CA = [[0] for i in range(len(channells))]
	ln_TC = [[0] for i in range(len(channells))]
	
	for i in range(len(channells)):
		ln_SV[i], = SenseV.plot(time_SV, SV[i], '-', label = channells[i])
		ln_TV[i], = TerminalV.plot(time_TV, TV[i], '-')

		ln_LP[i], = LoadP.plot(time_LP, LP[i], '-')
		ln_MP[i], = ModP.plot(time_MP, MP[i], '-')

		ln_CA[i], = CurrentA.plot(time_CA, CA[i], '-')
		ln_TC[i], = TempC.plot(time_TC, TC[i], '-')

	
	SenseV.legend(loc='center', bbox_to_anchor=(2.3,-0.7))

	SenseV.set_xlabel("time (s)")
	TerminalV.set_xlabel("time (s)")

	LoadP.set_xlabel("time (s)")
	ModP.set_xlabel("time (s)")

	CurrentA.set_xlabel("time (s)")
	TempC.set_xlabel("time (s)")

	SenseV.grid(True)
	TerminalV.grid(True)
	LoadP.grid(True)
	ModP.grid(True)
	CurrentA.grid(True)
	TempC.grid(True)

	SenseV.set_ylabel("Sense Voltage (V)")
	TerminalV.set_ylabel("Terminal Voltage (V)")

	LoadP.set_ylabel("Power of the Load (W)")
	ModP.set_ylabel("Power of the Module (W)")

	CurrentA.set_ylabel("Current (A)")
	TempC.set_ylabel("Temperature (C)")

	SVs = [0]
	TVs = [0]

	LPs = [0]
	MPs = [0]

	CAs = [0]
	TCs = [0]

	def ramp_up(rate,V,channel):
		mpod.setVoltageRiseRate(rate,channel)
		mpod.channelSwitch(1, channel)
		mpod.setVoltage(V,channel)

	def ramp_down(rate,V,channel):
		mpod.setVoltageFallRate(rate,channel)
		mpod.channelSwitch(1, channel)
		mpod.setVoltage(V,channel)


	####################
	# 				   #
	# Pre-Defined Func #
	#				   #
	####################

	def update(frame, channells,start):
		current = time.time()
		dt = current - start
		start = current
		time_lims = period(duration,dt)
		print(time_lims)
		for i in range(len(channells)):
			if i == 0:
				time_SV.append(dt)
				time_TV.append(dt)
				time_LP.append(dt)
				time_MP.append(dt)
				time_CA.append(dt)
				time_TC.append(dt)
				
				MP_lims = ax_lims(MPs)
				ModP.axis([time_lims[0], time_lims[1] + dt, MP_lims[0], MP_lims[1]])
				MP_tmp = float(mpod.getModulePower(channells))
				MP[i].append(MP_tmp)
				MPs.append(MP_tmp)
				ln_MP[i].set_data(time_MP, MP[i]) 
		
			SV_lims = ax_lims(SVs)
			SenseV.axis([time_lims[0], time_lims[1] + dt, SV_lims[0], SV_lims[1]])
			SV_tmp = float(mpod.getMeasurementSenseVoltage(channells[i]))
			SV[i].append(SV_tmp)
			SVs.append(SV_tmp)
			ln_SV[i].set_data(time_SV, SV[i]) 
			
			TV_lims = ax_lims(TVs)
			TerminalV.axis([time_lims[0], time_lims[1]+ dt, TV_lims[0], TV_lims[1]])
			TV_tmp = float(mpod.getMeasurementTerminalVoltage(channells[i]))
			TV[i].append(TV_tmp)
			TVs.append(TV_tmp)
			ln_TV[i].set_data(time_TV, TV[i])  
		   
		   
			LP_lims = ax_lims(LPs)
			LoadP.axis([time_lims[0], time_lims[1] + dt, LP_lims[0], LP_lims[1]])
			LP_tmp = float(mpod.getLoadPower(channells[i]))
			LP[i].append(LP_tmp)
			LPs.append(LP_tmp)
			ln_LP[i].set_data(time_LP, LP[i]) 
					   
			CA_lims = ax_lims(CAs)
			CurrentA.axis([time_lims[0], time_lims[1] + dt, CA_lims[0], CA_lims[1]])
			CA_tmp = float(mpod.getMeasurementCurrent(channells[i]))
			CA[i].append(CA_tmp)
			CAs.append(CA_tmp)
			ln_CA[i].set_data(time_CA, CA[i]) 
			
			TC_lims = ax_lims(TCs)
			TempC.axis([time_lims[0], time_lims[1] + dt, TC_lims[0], TC_lims[1]])
			TC_tmp = float(mpod.getMeasurementTemperature(channells[i]))
			TC[i].append(TC_tmp)
			TCs.append(TC_tmp)
			ln_TC[i].set_data(time_TC, TC[i])    
			
			f = open("./Logs/Measurement" + str(now) + ".log", "a")
			f.write("channel = " + channells[i] + "\t time = " + str(round(time_SV[-1],2)) + "\t V_S (V) = " + str(SV_tmp) + "\t V_T (V) = " + str(TV_tmp) + "\t P_L (W) = " + str(LP_tmp) + "\t P_M (W) = " + str(MP_tmp) + "\t I_L (A) = " + str(CA_tmp) + "\t T_L (C) = " + str(TC_tmp) + "\n")
			f.close()
			
		#return ln_SV[0]#,ln_TV,ln_LP,ln_MP,ln_CA,ln_TC,

	def period(T,t):
		if t > T:
			return t-T,dt
		else:
			return 0,t

	def ax_lims(list):
		if np.amax(list) < 0.05 and np.amin(list) == 0 :
			return -0.05, 0.05
		else:
			return np.amin(list)-0.05, np.amax(list)*1.1

	def Valid_channel():
		Valid = False
		while Valid == False:
			channel = input("Enter a Channel: ")
			for i in channels:
				if i == channel:
					Valid = True
			if Valid == False:
				print("Invalid Channel")
		return channel

	def view(channells):
		fig.suptitle("Measurements for channel " + str(channells))
		animation = FuncAnimation(fig, update, interval=100, fargs=(channells,time.time()-dt,))
		if save == False:
			plt.show(block = True)
		else:
			animation.save("./Logs/Animation" + str(now) + ".gif")
	
	view(channells)
	
def set_to_0(channells):
	for i in channells:
		mpod.setVoltage(0,i)
	
if __name__ == "__main__":

    # placeholder config file to define global variables
    conf = ConfigParser()
    conf.read("./config.ini")

    # define variables
    db = conf["DATABASE"]
    meta = conf["METADATA"]
    para = conf["PARAMETERS"]

    # initialize module #
    meta["MODULE"]

    # initialize MPOD class
    mpod = mpodPsu('192.168.196.6')

    #activation procedures
    mpod.mpodSwitch(1)
    channels = [".u0", ".u1", ".u2", ".u3", ".u100", ".u101", ".u102", ".u103", ".u104", ".u105", ".u106", ".u107"]
    channels = [".u2",".u3"]
    dt = 0
    
    channells = channels
    #set_to_0(channells)
    mpodviewer(channells)
    #set_to_0(channells)
    
    
	
