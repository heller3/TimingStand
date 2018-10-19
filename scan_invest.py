import time
import numpy as np
from numpy import loadtxt
import getpass
import os
import subprocess as sp
import socket
import sys

scan_number = raw_input('Give the scan number.')
channel_number = raw_input('Give the channel number (first channel is 0).')
position = raw_input('Give the position you want to investigate.')
scan_lines = [line.rstrip('\n') for line in open("/home/daq/Data/ScanRegistry/scan%d.txt"  % int(scan_number))]
vors = scan_lines[3]
if vors == 'vme':
    filename = "/home/daq/Data/AnalysisVME/processdata_" + scan_number + ".txt"
elif vors == 'scope':
    filename = "/home/daq/Data/AnalysisScope/processdata_" + scan_number + ".txt"
process_array = loadtxt(filename, delimiter=' ', unpack=False)
position_list = process_array[:,0].tolist()
value_search = min(position_list, key=lambda x:abs(x-float(position)))
index_position = position_list.index(float(value_search))
run_number = process_array[index_position,1]
print 'The run number is :', run_number
if vors == 'vme':
    isvme = 1
    command = '. /home/daq/TimingDAQ/dattorootpulse.sh /home/daq/Data/CMSTiming/RawDataSaver0CMSVMETiming_Run' + str(int(run_number)) + '_0_Raw.dat /home/daq/Data/CMSTiming/test' + str(int(run_number)) + '.root'
elif vors == 'scope':
    isvme = 0
    command = '. /home/daq/TimingDAQ/dattorootpulse.sh /home/daq/Data/NetScopeTiming/RawDataSaver0NetScope_Run' + str(int(run_number)) + '_0_Raw.dat /home/daq/Data/NetScopeTiming/test' + str(int(run_number)) + '.root'
os.system(command)

os.system(''' root -l 'plot_invest.c("%s",%d,"%s")' ''' % (str(int(run_number)),isvme, channel_number))

