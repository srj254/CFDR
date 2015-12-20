# CFDR
CFDR


This is the user guide for using the python source code present in this repository. These source files has dependency on following Python modules, please ensure these are installed in the environment.
 1. Pandas
 2. Matplotlib
 3. Numpy and Scipy
And it has interdependencies between themselves (you should have seen some *.pyc files among the *.py files). So keep the file and folder structure as is and use it from such a file structure to keep away from issues/glitches of accessing different modules. In addition to all these the raw workload data should be kept on the file system. Suitable configuration parameters are provided to make sure any path on file system can be pointed at. 

Each python source file when run without arguments gives the help on how to use it. For example, If the name of script is `getUniqueScripts.py` then running it without arguments would give,

    mydir$ ./getUniqueScripts.py
    Usage ./script.py JobScriptPath
    mydir$ 

In the above example, we see that `getUniqueScripts` is python file which tries to extract unique files among the files in a directory.  The script needs one argument indicating where are the files located (directory path). In this fashion, all the python files have been annotated with usage information. 
The `trial.py` scripts are meant for trials and all code is meant for scratch purposes. The folder `plotScripts` are for extracting plots using the parsed data that is extracted from the raw data. 



