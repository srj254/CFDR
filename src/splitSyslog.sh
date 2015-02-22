#!/usr/bin/sh 

grep -i -e 'hansen' syslog-20141031-20141102 | tee hansen_logs.txt
grep -i -e 'conte' syslog-20141031-20141102 | tee conte_logs.txt

