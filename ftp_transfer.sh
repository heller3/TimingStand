#!/bin/sh
HOST='192.168.133.60'
USER='ftp'
PASSWD=''
FILE=$1
Directory='home/lvuser/natinst/bin/'
ftp -n $HOST <<END_SCRIPT
quote USER $USER
quote PASS $PASSWD
binary
cd $Directory
get $FILE
quit
END_SCRIPT
mv ./$FILE /C_DRIVE/LABVIEW\ PROGRAMS\ AND\ TEXT\ FILES/
