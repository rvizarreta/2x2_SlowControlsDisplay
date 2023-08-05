#!~/home/acd/acdemo/gizmo-control/py3/bin/python3

# -----------------------------------------------------------
# Created : August 2022
# Author  : Vanessa Cerrone
# Usage   : python3 gizmo_write.py -d <debug>
# Example : python3 gizmo_write.py -d False
#
# Read values from the impedance monitor (GIZMO)
# - Make an ssh connection to GIZMO
# - Start the readout program - GIZMO.elf
# - Loop and read values via the shell
# - Store values in database (InfluxDB)
# -----------------------------------------------------------



import base64
import getpass
import os
import socket
import sys
import traceback
import time
import argparse

import warnings 
warnings.filterwarnings(action='ignore',module='.*paramiko.*')

import paramiko
from paramiko.py3compat import input
from influxdb import InfluxDBClient
from datetime import datetime 
import numpy as np 



def main(debug = False):

    port = 22
    hostname = 'lartf-gizmo01'
    username = 'root'
    password = ''

    # setup database 
    client_db = InfluxDBClient(host='localhost', port=8086, database = 'gizmo')
    client_db.create_database('gizmo')
    client_db.switch_database('gizmo')

    # lists to store parameters (resistance, threshold, magnitude, current, charge, time)
    r, th, m, i, q, t = [],[],[],[],[],[]

    # list to store data for influxdb
    json_payload = []

    try:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #client.set_missing_host_key_policy(paramiko.WarningPolicy())

            print('*** Connecting ...')
            client.connect(hostname, port, username, password)
            chan = client.invoke_shell() # Start an interactive shell session on the SSH server
            print('*** Start readout ... \n')
            chan.send('./GIZMO.elf 1\n') # Launch readout program


            while(1):
                time.sleep(2)
                line = chan.recv(1000).decode('ASCII').strip() # Receive data from the channel

                # Example of output line --> RES=154.8  TH=100 ( mag= 268.640, I= 265.217, Q= -42.746 )                         
                if 'RES' == line[0:3]:
                    now = datetime.utcnow().strftime('%Y%m%d %H:%M:%S') # UTC time to match InfluxDB time
                    print('Processing line = %s' % line)
                    line = line.replace('(', ' ')
                    line = line.replace(')', ' ')
                    line = line.replace('= ', '=')
                    line = line.replace(', ', ' ')
                    sl = line.split() # split line

                    RES, TH, mag, I, Q = [float(sl[i].split('=')[1]) for i in range(0,5)]

                    # Append data into lists to save in txt file (if debug = True)
                    params = [RES, TH, mag, I, Q, now]
                    [x.append(y) for x,y in zip([r, th, m, i, q, t], params)]

                    # Create dictionary to store data in InfluxDB 
                    data = {
                        'measurement' : 'LArTF_monitor',
                        'time' : now,
                        'fields' : {
                            'Res': RES,
                            'th' : TH,
                            'mag' : mag,
                            'I' : I,
                            'Q' : Q
                        }
            
                    }
                    json_payload.append(data)
                    # send payload
                    client_db.write_points(json_payload)
                    #print(now, RES, TH, mag, I, Q)

            chan.close()
            client.close()

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                client.close()
            except:
                pass
            sys.exit(1)

    except KeyboardInterrupt:
        print('\nData acquisition stopped')
        raise SystemExit


    # If debug = True open txt file to save data 
    if debug:
        path = '/home/acd/acdemo/gizmo-control/gizmo/'
        filename, _ = t[0].split()
    
        if os.path.exists(path + 'results/' + filename + '.txt'):
            print('File exists')
            outfile = open(path + 'results/' + filename + '.txt', 'a')

        else: 
            outfile = open(path + 'results/' + filename + '.txt', 'a')
            outfile.write('Time\t' + 'Res\t' + 'th\t' + 'mag\t' + 'I\t'+ 'Q\n')


        for k in range(0,len(r)):

            outfile.write( str(t[k]) + '\t' + str(r[k]) + '\t' + str(th[k]) + '\t' + 
                        str(m[k]) + '\t' +  str(i[k]) + '\t' + str(q[k]) + '\n' )

        # close file
        outfile.close()



def parse_args():
    '''Parse the args.'''
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '-debug',type = bool, required = False,
                        default = False,
                        help = 'Debug: save data in txt files')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(debug = args.d)




