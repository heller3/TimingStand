import time
import numpy as np
from numpy import loadtxt
import getpass
import os
import subprocess as sp
import socket
import sys
from datetime import datetime

### wait for certain time (modulo 60 seconds)
def wait_until(nseconds):
    while True:
        currentSeconds = datetime.now().time().second
        if abs(currentSeconds - nseconds)>0:
            time.sleep(0.1)
        else:
            break
    return


def set_env():
    #################SETTING THE ENVIRONMENT#########################
    #Mount network drive, source thisroot.sh, do startots
    print 'PREPARING THE ENVIRONMENT'
    time.sleep(2)
    print 'STARTING THE OTS-DAQ'
    time.sleep(2)
    os.system('. ~/otsdaq/build_slf7.x86_64/otsdaq/bin/StartOTS.sh')
    os.system('. /home/daq/Downloads/root/bin/thisroot.sh')
    print 'ROOT IS READY'
    os.system('sudo umount /media/network')
    os.system('sudo mount -a')
    print 'NETWORK DRIVE MOUNTED'

