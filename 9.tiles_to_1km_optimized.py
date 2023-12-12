# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 13:12:06 2023

@author: no67wuwu
work: convert all the tiles to 1km in a very optimized way using parallel processing.
"""

# Import libraries
import os
from glob import glob
# library to perform parallel processing
from concurrent.futures import ThreadPoolExecutor

# function ro perform the gdalwrap to set a diferenf resolutio; first to tr100 and the to tr1000
def process_file(f, path, outpath):
    name = f.split(os.sep)[-1]
    outname = os.path.join(outpath, name)
    
    cmd = 'gdalwarp -tr 1000 1000 -r mode -srcnodata 0 -co "Compression=deflate" {} {}'
    os.system(cmd.format(f, outname))
    
    return 'done with {}'.format(name)

# define the path
path = r'S:\Emmanuel_OcegueraConchas\eu_frga_forest\result_grass\eu_forest_frag_unique_masked_tr100'
outpath = r'S:\Emmanuel_OcegueraConchas\eu_frga_forest\result_grass\eu_forest_frag_unique_masked_tr1000'

# get all the tiles 
files = glob(os.path.join(path, '*.tif'))

# Use ThreadPoolExecutor to parallelize the process
with ThreadPoolExecutor(max_workers=20) as executor: # adapt to computer capacity
    results = executor.map(lambda f: process_file(f, path, outpath), files)

# print results
for result in results:
    print(result)

