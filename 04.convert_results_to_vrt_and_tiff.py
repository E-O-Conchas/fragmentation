# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 09:51:27 2023

@author: no67wuwu

Work: This script takes all the tifles from the results folder 
      and convert it to a vrt file and tiff files as output.
      After running this the tiff might need to be mask with euroepan union mask

"""

# Import libraries
from osgeo import gdal
import os


# Define the paths
# Directory containing TIFF files
directory = r'S:\User_name\result\window_count3'
# Output VRT file path
vrt_path = r'S:\User_name\result\window_count3.vrt'
# Output TIFF file path
tif_path = r"S:\User_name\result\name_to_the_tiff.tif"


# Get all TIFF files in the directory
tiff_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.tif')]

# Create VRT
vrt = gdal.BuildVRT(vrt_path, tiff_files)
vrt = None  # This will save and close the VRT file

# Convert VRT to GeoTIFF and export 
gdal.Translate(tif_path, vrt_path, format='GTiff')

print(f"VRT file saved at: {vrt_path}")
print(f"GeoTIFF file saved at: {tif_path}")
