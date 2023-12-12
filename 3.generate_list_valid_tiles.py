# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 16:05:56 2023

@author: no67wuwu
work: generate a list of a valid tiles from the combined tiles in the step 2
"""

import os

import subprocess

from glob import glob


# Define the function
def get_stdout(cmd, verbose=False):
    """
    send command to the commandline and fetch the return
    
    oprion verbose: will also print the return
    
    from http://blog.kagesenshi.org/2008/02/teeing-python-subprocesspopen-output.html
    """
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = []
    while True:
        line = p.stdout.readline()
        line = line.decode('utf-8') # Decode the bytes into a string
        line = line.replace('\n','').replace('\r','')
        if line != '':
            stdout.append(line)
        if verbose:
            print(line),
        if line == '' and p.poll() != None: #p.poll is checking if the process is still running
            break
    return stdout

# Define the pathe where all the combined files are
# path = r'S:\Emmanuel_OcegueraConchas\Fragmentation\frag_and_land\*.tif'
path = r"I:\biocon\Emmanuel_Oceguera\projects\2023_09_Fragmentation\estonia_forest_fragmentation\land_frag_combined\*.tif"

# get the list of all the files
files = glob(path)

# Define the gdal command 
cmd = 'gdalinfo -stats %s'

# Open a text file in writing modus. This file will be used to store the paths of the tif files that meet cetain criteria
vrt_imgs = open(r'I:\biocon\Emmanuel_Oceguera\projects\2023_09_Fragmentation\estonia_forest_fragmentation\valid_tiles.txt', 'w')

for f in files:
    stats = get_stdout(cmd %f)
    if not stats[0].startswith('ERROR'):
        vrt_imgs.write(f+'\n')
    else:
        print ('not considered: %s' %f.split(os.sep)[-1])
        
vrt_imgs.close()
