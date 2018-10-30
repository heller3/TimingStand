import time
import numpy as np
from numpy import loadtxt
import getpass
import os
import subprocess as sp
import socket
import sys
import glob


vmeRawDataDir = "/home/daq/Data/CMSTiming/"
scopeRawDataDir = "/home/daq/Data/NetScopeTiming/"
runRegistryDir = "/home/daq/Data/RunRegistry/"

def run_exists(run_number, vors):
    if vors == 'vme':
        rawPath = "%s/RawDataSaver0CMSVMETiming_Run%i_0_Raw.dat" % (vmeRawDataDir, run_number)
    if vors == 'scope':
        rawPath = "%s/RawDataSaver0NetScopeTiming_Run%i_0_Raw.dat" % (scopeRawDataDir, run_number)        
    return os.path.exists(rawPath)

def run_registry_exists(run_number):
    rawPath = "%s/run%i.txt" % (runRegistryDir, run_number)
    print rawPath
    return os.path.exists(rawPath)

def get_run_number():

    labview_max = max([int(x.split("/media/network/a/LABVIEW PROGRAMS AND TEXT FILES/time_")[1].split(".txt")[0]) for x in glob.glob("/media/network/a/LABVIEW PROGRAMS AND TEXT FILES/time_*")])
    otsmax = max([int(x.split("/home/daq/Data/RunRegistry/run")[1].split(".txt")[0]) for x in glob.glob("/home/daq/Data/RunRegistry/run*")])
    run_number = max(labview_max,otsmax)
    return run_number

def write_runfile(a, run_number, scan_number, vors, board_sn, bias_volt, laser_amp, laser_fre, amp_volt, scan_in, scan_stepsize, beam_spotsize, temp):
    runfile_handle = open("/home/daq/Data/RunRegistry/run%d.txt" % run_number, "a+") 
    runfile_handle.write(str(a) + "\n") #str(lab.motor_pos())
    runfile_handle.write(str(run_number)+ "\n")
    runfile_handle.write(str(scan_number)+ "\n")
    runfile_handle.write(vors+ "\n")
    runfile_handle.write(board_sn+ "\n")
    runfile_handle.write(bias_volt+ "\n")
    runfile_handle.write(laser_amp+ "\n")
    runfile_handle.write(laser_fre+ "\n")
    runfile_handle.write(amp_volt+ "\n")
    runfile_handle.write(scan_in+ "\n")
    runfile_handle.write(scan_stepsize+ "\n")
    runfile_handle.write(beam_spotsize+ "\n")
    runfile_handle.write(temp+ "\n")
    runfile_handle.close()

def write_scanfile(start_run_number, stop_run_number, scan_number, a, b, vors, board_sn, bias_volt, laser_amp, laser_fre, amp_volt, scan_in, scan_stepsize, beam_spotsize, temp):
    scanfile_handle = open("/home/daq/Data/ScanRegistry/scan%d.txt" % scan_number, "a+") 
    scanfile_handle.write(str(start_run_number)+ "\n")
    scanfile_handle.write(str(stop_run_number)+ "\n")
    scanfile_handle.write(str(scan_number)+ "\n")
    scanfile_handle.write(vors+ "\n")
    scanfile_handle.write(scan_in+ "\n")
    scanfile_handle.write(board_sn+ "\n")
    scanfile_handle.write(bias_volt+ "\n")
    scanfile_handle.write(laser_amp+ "\n")
    scanfile_handle.write(laser_fre+ "\n")
    scanfile_handle.write(amp_volt+ "\n")
    scanfile_handle.write(scan_stepsize+ "\n")
    scanfile_handle.write(beam_spotsize+ "\n")
    scanfile_handle.write(temp+ "\n")
    if scan_in == 'x' or scan_in == 'y':
        scanfile_handle.write(str(a)+ "\n") #Initial motor position
        scanfile_handle.write(str(b)+ "\n") #Final motor position
    elif scan_in == 't':
        scanfile_handle.write(str(a)+ "\n") #Single position
    scanfile_handle.close()

def append_scanfile(i, scan_number):
    scanfile_handle = open("/home/daq/Data/ScanRegistry/scan%d.txt" % scan_number, "a+") 
    scanfile_handle.write(i + "\n")
    scanfile_handle.close()

def process_runs(scan_number):
    print '############################PROCESSING RUNS#############################'
    #Calling a script to combine the trees and make text files for plotting.
    scan_lines = [line.rstrip('\n') for line in open("/home/daq/Data/ScanRegistry/scan%d.txt"  % scan_number)]
    start_run_number = scan_lines[0]
    stop_run_number = scan_lines[1]
    vors = scan_lines[3]
    if vors == 'vme':
        isvme = 1
    elif vors == 'scope':
        isvme = 0
    print 'Start run number: ', int(start_run_number)
    print 'Stop run number: ', int(stop_run_number)
    n_processed = 0
    for i in range (int(start_run_number), int(stop_run_number) + 1):   
        if run_exists(i) and run_registry_exists(i):       
            run_lines = [line.rstrip('\n') for line in open("/home/daq/Data/RunRegistry/run%d.txt"  % i)]
            motor_pos = run_lines[0]
            print 'Motor position: ', float(motor_pos)
            combineCmd = ''' root -l -q 'combine.c("%s",%d,%d,%f)' ''' % (str(i),scan_number,isvme, float(motor_pos))
            os.system(combineCmd)
            n_processed = n_processed + 1
    print 'Processed %i out of expected %i runs attempted in scan.' %(n_processed , int(stop_run_number)-int(start_run_number)+1)


def dattoroot(scan_number):
    print '############################CONVERTING TO ROOT FILES#############################'
    scan_lines = [line.rstrip('\n') for line in open("/home/daq/Data/ScanRegistry/scan%d.txt"  % scan_number)]
    start_run_number = scan_lines[0]
    stop_run_number = scan_lines[1]
    vors = scan_lines[3]
    if vors == 'vme':
        isvme = 1
        dattorootCmd = ". /home/daq/TimingDAQ/dattoroot.sh /home/daq/Data/CMSTiming/RawDataSaver0CMSVMETiming_Run%s_0_Raw.dat /home/daq/Data/CMSTiming/RawDataSaver0CMSVMETiming_Run%s_0_Raw.root" % ( run_number, run_number)        
    elif vors == 'scope':
        isvme = 0
        dattorootCmd = ". /home/daq/TimingDAQ/dattorootscope.sh /home/daq/Data/NetScopeTiming/RawDataSaver0NetScope_Run%s_0_Raw.dat /home/daq/Data/NetScopeTiming/RawDataSaver0NetScope_Run%s_0_Raw.root" %(run_number, run_number)
    print 'Start run number: ', int(start_run_number)
    print 'Stop run number: ', int(stop_run_number)
    n_processed = 0
    for i in range (int(start_run_number), int(stop_run_number) + 1):   
        if run_exists(i) and run_registry_exists(i):       
            os.system(dattorootCmd);
            n_processed = n_processed + 1
    print 'Converted %i out of expected %i runs attempted in scan.' % (n_processed , int(stop_run_number)-int(start_run_number)+1)


def analysis_plot(scan_number):
    scan_lines = [line.rstrip('\n') for line in open("/home/daq/Data/ScanRegistry/scan%d.txt"  % scan_number)]
    vors = scan_lines[3]
    if vors == 'vme':
        isvme = 1
    elif vors == 'scope':
        isvme = 0
    scan_in = scan_lines[4]
    if scan_in == 'x' or scan_in == 'y':
        istime = 0 
    elif scan_in == 't':
        istime = 1
    os.system(''' root -l 'plot.c(%d,%d,%d)' ''' % (scan_number,isvme, istime))
