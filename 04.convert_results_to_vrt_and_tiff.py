# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 09:51:27 2023

@author: no67wuwu

Work: This script takes all the tifles from the results folder 
      and convert it to a vrt file and tiff files as output.
      After running this the tiff might need to be mask with euroepan union mask

"""

from osgeo import gdal
import os

# Base directory
base_dir = r"S:\Emmanuel_OcegueraConchas\fragmentation_analysis\EUNIS"

# Define the habitats 
habitats = ["R34", "R42", 
            "R57", "S31", "S38", "S41", 
            "S42", "S93", "T13", "T22", 
            "T27", "T34"]

# Define the year
year = 2018

# Loop over habitats
for habitat in habitats:
    print(f"Processing habitat: {habitat}")
    
    # Define input directory and output paths
    directory = os.path.join(base_dir, habitat, str(year), 
                             "base_fragmentation_map2_EUNIS", 
                             "bfragmap2_meff_EUNIS", 
                             "window_count3")
                             
    vrt_path = os.path.join(base_dir, habitat, str(year), 
                            "base_fragmentation_map2_EUNIS", 
                            "bfragmap2_meff_EUNIS", 
                            "window_count3.vrt")
                            
    tif_path = os.path.join(base_dir, habitat, str(year), 
                            "base_fragmentation_map2_EUNIS", 
                            "bfragmap2_meff_EUNIS", 
                            f"{habitat}_{year}_bfragmap2_meff_eunis.tif")
    
    # Ensure directory exists
    if not os.path.exists(directory):
        print(f"Directory does not exist: {directory}")
        continue
    
    # Get all TIFF files in the directory
    tiff_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.tif')]
    
    if not tiff_files:
        print(f"No TIFF files found in directory: {directory}")
        continue
    
    print(f"Found {len(tiff_files)} TIFF files for {habitat}.")
    
    # Create VRT
    vrt = gdal.BuildVRT(vrt_path, tiff_files)
    vrt = None  # Save and close the VRT file
    
    print(f"VRT file created for {habitat} at: {vrt_path}")
    
    # Define arguments for GeoTIFF creation
    kwargs = {
        'format': 'GTiff',
        'outputType': gdal.GDT_UInt16
    }
    
    # Convert VRT to GeoTIFF
    gdal.Translate(tif_path, vrt_path, **kwargs)
    
    print(f"GeoTIFF file created for {habitat} at: {tif_path}")

print("Processing complete for all habitats.")


## Note: for now the code is working with the base_fragmentation_map2_EUNIS and bfragmap2_meff_EUNIS
##       but it can be easily modified to work with other maps and meff folders. This will be done in the future.
