import time
import numpy as np
from numpy import loadtxt
import getpass
import os
import subprocess as sp
import socket
import sys
import other_func.py as func
import labview_tools.py as lab
import TCP_com.py as tcp
import database_util.py as util


 
#USING VME OR SCOPE
vors = raw_input("VME (type vme) OR SCOPE (type scope)?") 
if vors == 'vme':
   isvme = 1
elif vors == 'scope':
   isvme = 0



#SPECIFY SCAN PARAMETERS
print '#####################SPECIFY SCAN PARAMETERS###################'
print 'Write everything with proper signs and without space. Type "NA" if you dont want to include the field in the name' 
board_sn = raw_input("Which board are you using?") 
bias_volt = raw_input("BIAS VOLTAGE (V) : ")
bias_volt = bias_volt + 'V'
laser_amp = raw_input("LASER AMPLITUDE : ")
laser_fre = raw_input("LASER FREQUENCY (kHz): ")
laser_fre = laser_fre + 'kHz'
amp_volt = raw_input("AMPLIFIER VOLTAGE (V): ")
amp_volt = amp_volt + 'V'
scan_in = raw_input("SCAN IN (options: 'x', 'y', 't'): ")
scan_stepsize = raw_input("SCAN STEP SIZE (mm): ")
scan_stepsize = scan_stepsize + 'mm'
beam_spotsize = raw_input("BEAM SPOT SIZE (um): ")
beam_spotsize = beam_spotsize + 'um'
temp = raw_input("TEMPERATURE_RES (kOhms): ")
temp = temp + 'kOhms'

#SETTING ENVIRONMENT
func.set_env()

#TELLING MOTOR WHICH SCAN TO DO
xory_handle = open("/media/network/a/LABVIEW PROGRAMS AND TEXT FILES/xory.txt", "w")
xory_handle.write(scan_in)
xory_handle.close()


#CONFIGURING AND INITIALIZING THE OTSDAQ
print 'INTITIALIZING THE OTS-DAQ'
tcp.init_ots()
print 'CONFIGURING THE OTS-DAQ'
tcp.config_ots()

scan_number = lab.scan_num() #Reading scan number
run_number = lab.run_num() + 1 #Reading run number (increment from where we left off) 
start_run_number = run_number
#Increment scan number in the text file
scan_write = open("/home/daq/Data/ScanRegistry/scan_number.txt", "w")
scan_write.write(str(scan_number + 1))
scan_write.close()



#SCAN IF LOOP
if scan_in == 'x' or scan_in == 'y':
        print '############################STARTING POSITION SCAN###############################'
        wait_for_file("/media/network/a/LABVIEW PROGRAMS AND TEXT FILES/otsstatus.txt", 1,'Waiting for motor to get to initial position')    
        i = 0 
        while i != 2:   
            print 'Motor moved to : ' lab.motor_pos()
            motor_pos_init = lab.motor_pos()
            time.sleep(20)
            tcp.start_ots(run_number) #start ots-daq
            time.sleep(20)
            #Writing run files
            util.write_runfile(lab.motor_pos(), run_number, scan_number, vors, board_sn, bias_volt, laser_amp, laser_fre, amp_volt, scan_in, scan_stepsize, beam_spotsize, temp)
            #Written run files
            tcp.stop_ots()  #stop otsdaq
            time.sleep(5)
            wait_for_file("/media/network/a/LABVIEW PROGRAMS AND TEXT FILES/motor.txt", 0,'Motor is still moving')
 
            #For the end run of the OTS-DAQ 
            motor_con = open("/media/network/a/LABVIEW PROGRAMS AND TEXT FILES/motor_con.txt", "r")
            i = int(motor_con.read()) + 1
            if i == 2:
                 print 'Motor moved to : ' lab.motor_pos()
                 run_number = run_number + 1
                 time.sleep(20)
                 tcp.start_ots(run_number) #start ots-daq
                 print 'RUNNING OTSDAQ FOR THE LAST TIME'
                 time.sleep(20)
                 #Writing run files
                 util.write_runfile(lab.motor_pos(), run_number, scan_number, vors, board_sn, bias_volt, laser_amp, laser_fre, amp_volt, scan_in, scan_stepsize, beam_spotsize, temp)
                 #Written run files
                 tcp.stop_ots()  #stop otsdaq                 
            run_number = run_number + 1    
            #Writing scan file    
            util.write_scanfile(start_run_number, run_number, scan_number, motor_pos_init, lab.motor_pos(), vors, board_sn, bias_volt, laser_amp, laser_fre, amp_volt, scan_in, scan_stepsize, beam_spotsize, temp):

motor_con.close()



elif scan_in == 't':
            print '############################STARTING TIME SCAN###########################'
            tot_time = raw_input("Give the scan time duration (in hrs).")
            motor_pos = raw_input("Enter the motor position.")            
            stop_scan = int(tot_time) * 3600/210
            time.sleep(20)
            while scan_counter != stop_scan:       
                scan_counter = scan_counter + 1
                tcp.start_ots(run_number) #start ots-daq
                #Writing run files
                util.write_runfile(float(motor_pos), run_number, scan_number, vors, board_sn, bias_volt, laser_amp, laser_fre, amp_volt, scan_in, scan_stepsize, beam_spotsize, temp)
                #Written run files                
                time.sleep(25)
                tcp.stop_ots()  #stop otsdaq
                time.sleep(170)
                run_number = run_number + 1
            #Writing scan file    
            util.write_scanfile(start_run_number, run_number, scan_number, motor_pos, motor_pos, vors, board_sn, bias_volt, laser_amp, laser_fre, amp_volt, scan_in, scan_stepsize, beam_spotsize, temp):



print '######################################SCAN COMPLETE#######################################'


#SCAN STATUS
print 'Start run number: ', start_run_number
print 'Stop run number: ', run_number 
print 'Total runs taken: ',  run_number - start_run_number + 1

#PROCESS RUNS
util.process_runs(scan_number)

#PLOT DATA
util.analysis_plot(scan_number)
