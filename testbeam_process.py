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
    #Define base paths for labview file, root file, pixel file, timestamp file
    labview_unsync_base_path = "" 
    labview_sync_base_path = "" 
    pixel_base_path = ""
    if(isvme):
        root_base_path = ""
        timestamp_base_path = ""
    else:
        root_base_path = ""
        timestamp_base_path = ""
    
    #Absolute file paths
    labview_sync_abs_path = labview_sync_base_path + "lab_meas_sync_%d.txt" % run_number
    pixel_abs_path = pixel_base_path + "/pixel_%d.txt" % run_number
    if(isvme):
        root_abs_path = root_base_path + "/RawDataSaver0CMSVMETiming_Run%d_0_Raw.root" % run_number
        timestamp_abs_path = timestamp_base_path + "/timestamp%d.txt" % run_number
    else:    
        root_abs_path = root_base_path + "/RawDataSaver0NetScope_Run%d_0_Raw.root" % run_number
        timestamp_abs_path = timestamp_base_path + "/timestamp%d.txt" % run_number

    
    #sync labview data
    db.new_sync_labview_files(labview_sync_abs_path, timestamp_abs_path, labview_unsync_base_path)
    print 'Done syncing labview data for run ', run_number

    #call combine script for labview
    os.system(''' root -l 'lab_combine_testbeam.c("%s","%s")' ''' % (root_abs_path, labview_sync_abs_path))
    print 'Combined labview data with the root file for run ', run_number

    #call combine script for pixel
    os.system(''' root -l 'pixel_combine_testbeam.c("%s","%s")' ''' % (root_abs_path, pixel_abs_path))
    print 'Combined pixel data with the root file for run ', run_number
