import time
import numpy as np
from numpy import loadtxt
import getpass
import os
import subprocess as sp
import socket
import sys


def wait_for_file(filename, l, message=""):
 status_file = open(filename, "r")
 counter = 0
 while int(status_file.read()) != l:
  status_file.close()
  time.sleep(1)
  status_file = open(filename, "r")
  if message !="" and counter % 10 == 0 : print message
  counter = counter + 1
 status_file.close() 

def motor_pos():
 motor_pos = open("/media/network/a/LABVIEW PROGRAMS AND TEXT FILES/motorpos.txt", "r")
 position  = float(motor_pos.read())
 motor_pos.close()
 return position

def run_num():
 run_number = open("/media/network/a/LABVIEW PROGRAMS AND TEXT FILES/run.txt", "r")
 run  = int(run_number.read())
 run_number.close()
 return run

def scan_num():
 scan_number = open("/home/daq/Data/ScanRegistry/scan_number.txt", "r")
 scan  = int(scan_number.read())
 scan_number.close()
 return scan

