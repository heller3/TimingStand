import time
import numpy as np
from numpy import loadtxt
import getpass
import os
import subprocess as sp
import socket
import sys
from other_func import set_env
from database_util import dattoroot

scan_number = raw_input('Give the scan number: ')
dattoroot(int(scan_number))
