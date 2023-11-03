# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 16:25:58 2023

@author: no67wuwu


work: combine the rasters to get the final fragmentation with land

"""
#%%
import sys
sys.path.insert(0,r"I:\biocon\Emmanuel_Oceguera\projects\2023_03_NaturaConnect\tools")
import MacPyver as mp
#%%
import os
from glob import glob
import numpy as np

frag_path = r"S:\Emmanuel_OcegueraConchas\fragmentation_estonia_test\frag_raster"
land_path = r"S:\Emmanuel_OcegueraConchas\fragmentation_estonia_test\land_raster"
out_path = r"S:\Emmanuel_OcegueraConchas\fragmentation_estonia_test\frag_and_land"

# Get a list of tile filenames
tiles = [x[-15:] for x in glob(frag_path + os.sep + '*.tif')]

for t in tiles:
    frag_p = frag_path + os.sep + 'frag_tile_' + t
    land_p = land_path + os.sep + 'mask_tile_' + t
    
    frag = mp.raster.tiff.read_tif(frag_p)
    land = mp.raster.tiff.read_tif(land_p)
    
    out = np.where((frag==9) & (land==1), 9, land)
    
    mp.raster.tiff.write_tif(frag_p, out_path + os.sep + 'lf_comb_' + t, out, 6, nodata=0, option="COMPRESS=DEFLATE")

#%%
# # Import necessary libraries
# import os
# from glob import glob
# import numpy as np

# # Define the paths for input rasters and output directory
# frag_path = r"S:\Emmanuel_OcegueraConchas\Fragmentation\frag_raster"
# land_path = r"S:\Emmanuel_OcegueraConchas\Fragmentation\land_raster"
# out_path = r"S:\Emmanuel_OcegueraConchas\Fragmentation\frag_land"

# # Get a list of tile filenames
# tiles_2 = [os.path.basename(x) for x in glob(os.path.join(frag_path, '*.tif'))]

# # Loop through the tiles and combine the rasters
# for t in tiles:
#     frag_p = os.path.join(frag_path, 'frag_tile_' + t)
#     land_p = os.path.join(land_path, 'mask_tile_' + t)
#     out_p = os.path.join(out_path, 'lf_comb_' + t)

#     # Read the frag and land rasters
#     frag = mp.raster.tiff.read_tif(frag_p)
#     land = mp.raster.tiff.read_tif(land_p)

#     # Combine the rasters
#     out = np.where((frag == 9) & (land == 1), 9, land)

#     # Write the combined raster to the output directory
#     mp.raster.tiff.write_tif(frag_p, out_p, out, 6, nodata=0, option="COMPRESS=DEFLATE")
