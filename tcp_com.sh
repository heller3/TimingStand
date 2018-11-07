#!/bin/sh
if [ $1 == 'stop' ]
then
   echo 'stop'>/dev/tcp/169.254.249.145/10000
elif [ $1 = 'start' ]
then
   echo 'start'>/dev/tcp/169.254.249.145/10000
elif [ $1 = 'send_run_number' ]
then
   FILE1=$2
   echo $FILE1>/dev/tcp/169.254.249.145/10000
fi


