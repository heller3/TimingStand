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

#system arguments
isvme = sys.argv[1] #VME or NetScope
folder = sys.argv[2] #Folder name inside RECO

#Define base paths for labview file, reco file, pixel file, timestamp file
labview_unsync_base_path = "/eos/uscms/store/user/cmstestbeam/BTL_ETL/2018_11/data/Labview/Labview_unsync/" 
labview_sync_base_path = "/eos/uscms/store/user/cmstestbeam/BTL_ETL/2018_11/data/Labview/Labview_sync/" 
timestamp_base_path = "/eos/uscms/store/user/cmstestbeam/BTL_ETL/2018_11/data/Labview/Ots_Timestamp/"
reco_base_path = "/eos/uscms/store/user/cmstestbeam/BTL_ETL/2018_11/data/%s/RECO/%s/" % (isvme,folder) 
lab_reco_base_path = "/eos/uscms/store/user/cmstestbeam/BTL_ETL/2018_11/data/%s/RECO/%s_Labview/" % (isvme,folder)


while(1):
	        #sets containing run numbers from labview reco folder and reco folder
	        set_reco = set([int(x.split("Data%sTiming_Run" % isvme)[1].split(".root")[0].split("_")[0]) for x in glob.glob(reco_base_path + 'Data%sTiming*' % isvme)])
	        set_lab_reco = set([int(x.split("Data%sTiming_Run" % isvme)[1].split(".root")[0].split("_")[0]) for x in glob.glob(lab_reco_base_path + 'Data%sTiming*' % isvme)])
	        set_toprocess = set_reco - set_lab_reco

                #list containing all the file names from reco folder
	        #list_reco = [x for x in glob.glob(reco_base_path + 'Data%sTiming*') % isvme]

	        if len(set_toprocess) == 0:
			print 'No runs to process for the %s' % isvme	

		for x in set_toprocess:
                        #Absolute file paths
			labview_sync_abs_path = labview_sync_base_path + "lab_meas_sync_%d.txt" % x
			timestamp_abs_path = timestamp_base_path + "timestamp%d.txt" % x	        
                        #Sync labview data
			db.new_sync_labview_files(labview_sync_abs_path, timestamp_abs_path, labview_unsync_base_path)
			print 'Done syncing labview data for run ', x

			lab_reco_abs_path = lab_reco_base_path + "Data%sTiming_Run%d.root" % (isvme,x)
			reco_abs_path = reco_base_path + "Data%sTiming_Run%d.root" % (isvme,x)

                        #Create reco backup files for vme 
			os.system('cp %s %s' % (reco_abs_path, lab_reco_abs_path))   
 
                        #call combine script for labview
			os.system(''' root -l -q 'lab_combine_testbeam.c("%s","%s")' ''' % (lab_reco_abs_path, labview_sync_abs_path))
			print 'Combined labview data with the reco file for run ', x

		time.sleep(20)		



