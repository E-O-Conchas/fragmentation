# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 15:35:02 2023

@author: no67wuwu

work: we delete the tiles that dont have any information or No data
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
                                            #is it is running it returns None
            break
    return stdout



path = r'S:\Emmanuel_OcegueraConchas\eu_frga_forest\result_grass\eu_forest_frag_unique_masked\*.tif'

files = glob(path)

for f in files:
    cmd = 'gdalinfo -stats %s'
    cmd_ret = get_stdout(cmd % f)
    if 'NoData Value' in cmd_ret[-1]:
        os.remove(f)
        print("removed file: " + f.split(os.sep)[-1]) # print the file name only (without the path)

        