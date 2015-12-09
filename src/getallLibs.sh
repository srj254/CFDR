#!/bin/bash


#STR="Sarah;Lisa;Jack;Rahul;Johnson"  #String with names
STR="`cat ./myLdLibPath.txt`"
IFS=':' read -ra MY_PATHS <<< "$STR"    #Convert string to array

#Print all names from array
for i in "${MY_PATHS[@]}"; do
    #echo $i
    find $i -name "*.so" >> allPreInsLibs_modLoad.txt
done
