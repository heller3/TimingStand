import time
import numpy as np
from numpy import loadtxt
import getpass
import os
import subprocess as sp
import socket
import sys
from other_func import set_env
from database_util import process_runs

scan_number = raw_input('Give the scan number: ')
cmd = 'rm /home/daq/Data/AnalysisVME/processdata_' + scan_number + '.txt' 
os.system(cmd) 
process_runs(int(scan_number))
