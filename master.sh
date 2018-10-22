#!/bin/bash
if [ $1 == 'scan' ]
then
   python spacetime_scan.py
elif [ $1 = 'process' ]
then
   python process.py
elif [ $1 = 'plot' ]
then
   python plot.py
elif [ $1 = 'summary' ]
then
   python scan_invest.py
elif [ $1 = 'dattoroot' ]
then
   python dattoroot.py
fi

