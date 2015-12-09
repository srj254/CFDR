#!/bin/bash

#!/bin/bash
filename='./allModules'
echo Start
while read p; do 
    module load $p;
done < $filename

echo $LD_LIBRARY_PATH > myLdLibPath.txt
echo $PATH > myPath.txt
