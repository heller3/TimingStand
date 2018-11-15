import time
import numpy as np
from numpy import loadtxt
import getpass
import os
import subprocess as sp
import socket
import sys
import database_util as db
import glob

def check(list_to_check):
    bool = True
    for element in list_to_check:
        if not element.isdigit():
             print 'Removing %s element in the list' % element
             list_to_check.remove(element)
             bool = False             
    return bool, list_to_check

#Parsing arguments
parser = argparse.ArgumentParser(description='Information for running the labview reconstruction program')
parser.add_argument('--filename', metavar='filename', type=str, default = 'DataVMETiming_Run', help='Full filename before the run number', required=True)
parser.add_argument('--run_number', metavar='run_number', type=int, help='The run number', required=True)
parser.add_argument('--labview_unsync_base_path', metavar='labview_unsync_base_path', type=str, default= "/home/otsdaq/CMSTiming_Labview/LabviewUnsyncFiles/", help = 'Labview base path for unsync files (include / at the end)',required=False)
parser.add_argument('--labview_sync_base_path', metavar='labview_sync_base_path', type=str, default= "/home/otsdaq/CMSTiming_Labview/LabviewSyncFiles/", help = 'Labview base path for sync files (include / at the end)',required=False)
parser.add_argument('--timestamp_base_path', metavar='timestamp_base_path', type=str, default= "/data/TestBeam/2018_11_November_CMSTiming/VMETimestamp/", help = 'Base path for OTS-DAQ Timestamp files (include / at the end)',required=False)
parser.add_argument('--reco_base_path', metavar='reco_base_path', type=str, default= "/data/TestBeam/2018_11_November_CMSTiming/RECO/v2/", help = 'Base path for reconstructed run files (include / at the end)',required=False)
parser.add_argument('--lab_reco_base_path', metavar='lab_reco_base_path', type=str, default= "/data/TestBeam/2018_11_November_CMSTiming/RECO/v2_labview", help = 'Base path for final reconstructed files with labview readings (include / at the end)', required=False)

args = parser.parse_args()
filename = args.filename
run_number = args.run_number
labview_unsync_base_path = args.labview_unsync_base_path
labview_sync_base_path = args.labview_sync_base_path
timestamp_base_path = args.timestamp_base_path
reco_base_path = args.reco_base_path
lab_reco_base_path = args.lab_reco_base_path

while(1):
    
                #list of all the run numbers 
                list_reco_to_check = [(x.split(filename)[1].split(".root")[0].split("_")[0]) for x in glob.glob('%s%s*' % (reco_base_path, filename))]
                list_lab_reco = [(x.split(filename)[1].split(".root")[0].split("_")[0]) for x in glob.glob('%s%s*' % (lab_reco_base_path, filename))]
                
                #Check if the list is fine
                bool, list_reco = check(list_reco_to_check)
                if(bool):
                    print 'The Filenames in the list are fine.'
                else:
                    print 'Filenames in the list are screwed up, not processing bad file names!!!!!!!!!!!!!!'
                    time.sleep(5)

	        #sets containing run numbers from labview reco folder and reco folder
	        set_reco = set([int(x) for x in list_reco])
	        set_lab_reco = set([int(x) for x in list_lab_reco])
	        set_toprocess = set_reco - set_lab_reco

	        if len(set_toprocess) == 0:
			print 'No runs to process.'	

		for x in set_toprocess:
                        #Absolute file paths
			labview_sync_abs_path = "%slab_meas_sync_%d.txt" % (labview_sync_base_path,x)
			timestamp_abs_path = "%stimestamp%d.txt" % (timestamp_base_path,x)
	        
                        #Sync labview data
			db.new_sync_labview_files(labview_sync_abs_path, timestamp_abs_path, labview_unsync_base_path)
			print 'Done syncing labview data for run ', x

			lab_reco_abs_path = "%sDataVMETiming_Run%d.root" % (lab_reco_base_path,x)
			reco_abs_path = "%sDataVMETiming_Run%d.root" % (reco_base_path,x)

                        #Create reco backup files for vme 
			os.system('cp %s %s' % (reco_abs_path, lab_reco_abs_path))   
 
                        #call combine script for labview
			os.system(''' root -l -q 'lab_combine_testbeam.c("%s","%s")' ''' % (lab_reco_abs_path, labview_sync_abs_path))
			print 'Combined labview data with the reco file for run ', x

		time.sleep(20)		



