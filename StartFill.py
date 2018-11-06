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
#from database_util import run_registry_exists, run_exists,write_runfile, append_scanfile, write_scanfile, process_runs, analysis_plot, get_run_number, append_scanfile, dattoroot
from datetime import datetime

import database_util as db
import other_func as of 


debug = False
pixel = False

############# Important ##############
## This parameter defines at what time it is safe to start a new run
## It should be about 30 seconds before the arrival time of each spill 
## Since spills come every minute, this is defined as a number of seconds after the start of each clock minute (only meaningful modulo 60 seconds)
## Periodically make sure this value makes sense.
start_seconds = 30

stop_seconds = 20

### number of spills per run (approx number of minutes per run)
n_spills_per_run = 1

#SETTING ENVIRONMENT, starting OTSDAQ
if not debug: set_env()

#CONFIGURING AND INITIALIZING THE OTSDAQ
print 'INTITIALIZING THE OTS-DAQ'
if not debug: init_ots()
print 'CONFIGURING THE OTS-DAQ'
if not debug: 
	config_ots()
	time.sleep(40)

##Assign fill number
fill_number = db.get_next_fill_num() 
db.increment_fill_num() # for next time

print 'Fill number: ', fill_number

#Get first run number 
run_number = db.get_next_run_number()

while True:
	#### wait for safe time to start run ###
	of.wait_until(start_seconds)
	
	## start run
	print "Starting run %i at %s" % (run_number, datetime.now().time())
	if not debug: start_ots(run_number,False)

	## record run file for database
	db.write_short_runfile(fill_number,run_number)
	db.append_fillfile(fill_number,run_number)

	#Starting pixel tracker
	if pixel: os.system('source /home/daq/pixel.sh start')

	#Sending run number to pixel tracker
	if pixel: os.system('source /home/daq/pixel.sh send_run_number %d' % (run_number))

	### sleep for number of complete minutes per run
	time.sleep(60*(n_spills_per_run-1))

	## for last minute of run, wait until stop time
	of.wait_until(stop_seconds)
	print "Stopping run %i at %s" % (run_number, datetime.now().time())
	if not debug: stop_ots(False)

	#Stopping pixel tracker
	if pixel: os.system('source /home/daq/stop_pixel.sh stop')

	run_number = run_number+1 








