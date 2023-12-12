# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 09:51:27 2023

@author: no67wuwu
"""

from osgeo import gdal
import os

# Directory containing TIFF files
directory = r'S:\Emmanuel_OcegueraConchas\eu_fragmentation_forest\result\window_count3'

# Output VRT file path
vrt_path = r'S:\Emmanuel_OcegueraConchas\eu_fragmentation_forest\result\window_count3.vrt'

# Get all TIFF files in the directory
tiff_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.tif')]

# Create VRT
vrt = gdal.BuildVRT(vrt_path, tiff_files)
vrt = None  # This will save and close the VRT file
