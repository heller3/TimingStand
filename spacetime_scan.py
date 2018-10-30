import time
import numpy as np
from numpy import loadtxt
import getpass
import os
import subprocess as sp
import socket
import sys
import glob
from other_func import set_env
from labview_tools import wait_for_file, motor_pos, run_num, scan_num
from TCP_com import init_ots, config_ots, start_ots, stop_ots #in-built 5s delay in all of them
from database_util import run_registry_exists, run_exists,write_runfile, append_scanfile, write_scanfile, process_runs, analysis_plot, get_run_number, append_scanfile, dattoroot


 
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
set_env()

#TELLING MOTOR WHICH SCAN TO DO
xory_handle = open("/media/network/a/LABVIEW PROGRAMS AND TEXT FILES/xory.txt", "w")
xory_handle.write(scan_in)
xory_handle.close()


#CONFIGURING AND INITIALIZING THE OTSDAQ
print 'INTITIALIZING THE OTS-DAQ'
init_ots()
print 'CONFIGURING THE OTS-DAQ'
config_ots()
time.sleep(40) #remove this later

scan_number = scan_num() #Reading scan number
print 'Scan number: ', scan_number
#run_number = run_num() + 1 #Reading run number (increment from where we left off) 

#Increment scan number in the text file
scan_write = open("/home/daq/Data/ScanRegistry/scan_number.txt", "w")
scan_write.write(str(scan_number + 1))
scan_write.close()

#Run Number 
run_number = get_run_number() + 1
start_run_number = run_number

#SCAN IF LOOP
if scan_in == 'x' or scan_in == 'y':
        print '############################STARTING POSITION SCAN###############################'
        wait_for_file("/media/network/a/LABVIEW PROGRAMS AND TEXT FILES/otsstatus.txt", 1,'Waiting for motor to get to initial position')    
        motor_pos_init = motor_pos()
        i = 0 
        while i != 2:   
            print 'Motor moved to : ', motor_pos()

            #time.sleep(10)
            print 'Run Number: ', run_number
            if(run_exists(run_number, vors)): 
                print "ERROR: this run number already exists. Exiting!"
                break

            start_ots(run_number) #start ots-daq
            #time.sleep(5)
            stop_ots()  #stop otsdaq
            #time.sleep(10)
            
            #Writing run files
            if run_exists(run_number, vors):
                write_runfile(motor_pos(), run_number, scan_number, vors, board_sn, bias_volt, laser_amp, laser_fre, amp_volt, scan_in, scan_stepsize, beam_spotsize, temp)
            else:
                print "Run %i failed." % run_number

            wait_for_file("/media/network/a/LABVIEW PROGRAMS AND TEXT FILES/motor.txt", 0,'Motor is still moving')
 
            #For the end run of the OTS-DAQ 
            motor_con = open("/media/network/a/LABVIEW PROGRAMS AND TEXT FILES/motor_con.txt", "r")
            i = int(motor_con.read()) + 1
            if i == 2:
                 print 'Motor moved to : ', motor_pos()
                 run_number = run_number + 1
                 time.sleep(20)
                 print 'Run Number: ',run_number
                 print 'RUNNING OTSDAQ FOR THE LAST TIME'

                 start_ots(run_number) #start ots-daq
                 #time.sleep(5)
                 stop_ots()  #stop otsdaq                 

                 #Writing run files
                 if run_exists(run_number, vors):
                    write_runfile(motor_pos(), run_number, scan_number, vors, board_sn, bias_volt, laser_amp, laser_fre, amp_volt, scan_in, scan_stepsize, beam_spotsize, temp)
                 else:
                    print "Run %i failed." % run_number

            run_number = run_number + 1    

        write_scanfile(start_run_number, run_number - 1, scan_number, motor_pos_init, motor_pos(), vors, board_sn, bias_volt, laser_amp, laser_fre, amp_volt, scan_in, scan_stepsize, beam_spotsize, temp)
        motor_con.close()

elif scan_in == 't':
            print '############################STARTING TIME SCAN###########################'
            tot_time = raw_input("Give the scan time duration (in hrs).")
            motor_pos = raw_input("Enter the motor position.")            
            stop_scan = int(float(tot_time) * 3600/75) #should be 210
            scan_counter = 0
            while scan_counter != stop_scan:       
                time.sleep(25)
                scan_counter = scan_counter + 1
                start_ots(run_number) #start ots-daq
                #Writing run files
                write_runfile(float(motor_pos), run_number, scan_number, vors, board_sn, bias_volt, laser_amp, laser_fre, amp_volt, scan_in, scan_stepsize, beam_spotsize, temp)
                #Written run files                
                time.sleep(10)
                stop_ots()  #stop otsdaq
                time.sleep(10) #should be 170
                run_number = run_number + 1
            #Writing scan file    
            write_scanfile(start_run_number, run_number - 1, scan_number, motor_pos, motor_pos, vors, board_sn, bias_volt, laser_amp, laser_fre, amp_volt, scan_in, scan_stepsize, beam_spotsize, temp)



print '######################################SCAN COMPLETE#######################################'


#SCAN STATUS
print 'Start run number: ', start_run_number
print 'Stop run number: ', run_number - 1
print 'Total runs taken: ',  run_number - start_run_number 

for i in range(start_run_number, run_number):
    if not run_registry_exists(i):
        print 'No run file found for run number: ', i  
    #else:
        ################# REWRITE ####################
     #   print 'Appending scan file to include this run number', append_scanfile(i, scan_number)

#DATTOROOT
dattoroot(scan_number)

#PROCESS RUNS
process_runs(scan_number)

#PLOT DATA
analysis_plot(scan_number)


