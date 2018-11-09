import time
import numpy as np
from numpy import loadtxt
import getpass
import os
import subprocess as sp
import socket
import sys
import database_util as db

def testbeam_combine(run_number, isvme):
    os.system('source /cvmfs/sft.cern.ch/lcg/releases/LCG_88/ROOT/6.08.06/x86_64-slc6-gcc49-opt/bin/thisroot.sh')
    #Define base paths for labview file, root file, pixel file, timestamp file
    labview_unsync_base_path = '/eos/uscms/store/user/cmstestbeam/BTL_ETL/2018_11/data/Labview/Labview_unsync/' 
    labview_sync_base_path = "/eos/uscms/store/user/cmstestbeam/BTL_ETL/2018_11/data/Labview/Labview_sync/" 
    #pixel_base_path = ""

    if(isvme):
        root_base_path = "/eos/uscms/store/user/cmstestbeam/BTL_ETL/2018_11/data/VME/RECO/v1/"
        root_base_backup_path = "/eos/uscms/store/user/cmstestbeam/BTL_ETL/2018_11/data/VME/RECO/v1_backup_labview/"
        timestamp_base_path = "/eos/uscms/store/user/cmstestbeam/BTL_ETL/2018_11/data/Labview/Ots_Timestamp/"
    else:
        root_base_path = "/eos/uscms/store/user/cmstestbeam/BTL_ETL/2018_11/data/NetScope/RECO/v0/"
        root_base_backup_path = "/eos/uscms/store/user/cmstestbeam/BTL_ETL/2018_11/data/NetScope/v0_backup_labview/"
        timestamp_base_path = "/eos/uscms/store/user/cmstestbeam/BTL_ETL/2018_11/data/Labview/Ots_Timestamp/"
    
    #Absolute file paths
    labview_sync_abs_path = labview_sync_base_path + "lab_meas_sync_%d.txt" % run_number
    #pixel_abs_path = pixel_base_path + "/pixel_%d.txt" % run_number
    if(isvme):
        root_abs_backup_path = root_base_backup_path + "DataVMETiming_Run%d.root" % run_number
        root_abs_path = root_base_path + "DataVMETiming_Run%d.root" % run_number
        timestamp_abs_path = timestamp_base_path + "timestamp%d.txt" % run_number
    else:
        root_abs_backup_path = root_base_backup_path + "RawDataSaver0NetScope_Run%d_0_Raw.root" % run_number
        root_abs_path = root_base_path + "RawDataSaver0NetScope_Run%d_0_Raw.root" % run_number
        timestamp_abs_path = timestamp_base_path + "timestamp%d.txt" % run_number

    #create root backup files 
    os.system('cp %s %s' % (root_abs_path, root_abs_backup_path))    

    #sync labview data
    db.new_sync_labview_files(labview_sync_abs_path, timestamp_abs_path, labview_unsync_base_path)
    print 'Done syncing labview data for run ', run_number

    #call combine script for labview
    os.system(''' root -l 'lab_combine_testbeam.c("%s","%s")' ''' % (root_abs_backup_path, labview_sync_abs_path))
    print 'Combined labview data with the root file for run ', run_number

    #call combine script for pixel
    #os.system(''' root -l 'pixel_combine_testbeam.c("%s","%s")' ''' % (root_abs_path, pixel_abs_path))
    #print 'Combined pixel data with the root file for run ', run_number
