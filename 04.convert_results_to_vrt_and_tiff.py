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
base_dir = r"S:\Emmanuel_OcegueraConchas\fragmentation_analysis\EUNIS\R"


# Habitats that have beedn done already
# R31, R34, R42, R51, R57
habitats = [
"R11", "R12", "R13", "R14", "R15", "R16", "R17", "R18", "R19", "R1A", "R1B", "R1C",
"R1D", "R1E", "R1F", "R1G", "R1H", "R1J", "R1K", "R1L", "R1M", "R1N", "R1P", "R1Q",
"R1R", "R1S", "R21", "R22", "R23", "R24", "R32", "R33", "R35", "R36", "R37", "R41", 
"R43", "R44", "R45", "R52", "R53", "R54", "R55", "R56", "R61", "R62", "R63", "R64", 
"R65", "R73"]

# Define the year
year = 2018

# Loop over habitats
for habitat in habitats[0:1]:
    print(f"Processing habitat: {habitat}")
    
    # Define input directory and output paths
    directory = os.path.join(base_dir, habitat, str(year), 
                             "base_fragmentation_map2_EUNIS", 
                             "bfragmap2_meff_EUNIS", 
                             "window_count3")
                             
                            
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
    
    # Create VRT temorary
    vrt = gdal.BuildVRT('', tiff_files)
    
    # Define arguments for GeoTIFF creation
    kwargs = {
        'format': 'GTiff',
        'outputType': gdal.GDT_UInt16 # Maybe find anothre type it fit tou our data and take less space? 
    }
    
    # Convert VRT to GeoTIFF
    gdal.Translate(tif_path, vrt, **kwargs)
    
    print(f"GeoTIFF file created for {habitat} at: {tif_path}")

print("Processing complete for all habitats.")


## Note: for now the code is working with the base_fragmentation_map2_EUNIS and bfragmap2_meff_EUNIS
##       but it can be easily modified to work with other maps and meff folders. This will be done in the future.
