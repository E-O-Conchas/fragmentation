
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
input_base = r"D:\Emmanuel_Oceguera\Fragmentation_analysis\output\EUNIS"

# Base output directory (where mosaicked TIFFs will be stored)
output_base = r"D:\Emmanuel_Oceguera\Fragmentation_analysis\output\EUNIS"

# Define the year
year = 2012

habitats_groups = ['N', 'Q', 'R', 'S', 'T', 'U', 'V']

for group in habitats_groups[1:2]:
    print(f"Processing group: {group}")
    group_dir = os.path.join(input_base, str(year), group)
    if not os.path.exists(group_dir):
        print(f"Group folder does not exist: {group_dir}")
        continue
    
    #for habitat in os.listdir(group_dir):
    for i, habitat in enumerate(sorted(os.listdir(group_dir)), 1):
        # if habitat not in ['Q11', 'Q12','Q21','Q22','Q23']:  # Uncomment this line to filter habitats
        #     continue # Skip habitat not in the list

        print(f"[{i}/{len(os.listdir(group_dir))}] Processing habitat: {habitat}")
        habitat_dir = os.path.join(group_dir, habitat, "window_count3")
        if not os.path.exists(habitat_dir):
            continue
        
        print(f"processing habitat: {habitat}")
        
        # Get all tiff tiles
        
        tiff_tiles = [os.path.join(habitat_dir, f) for f in os.listdir(habitat_dir) if f.endswith(".tif")]
        
        if not tiff_tiles:
            print(f"No TIFF files found in: {habitat_dir}")
            continue
        
        
        print(f"found {len(tiff_tiles)} tiles for {habitat}")
        
        # we create the ouput folder
        output_path = os.path.join(group_dir, habitat, f"{habitat}_{str(year)}_mosaic.tiff")
          
        # Create VRT temorary
        vrt = gdal.BuildVRT('', tiff_tiles)
        
        print("VRT file has been created temporary...")
        
        # Define arguments for GeoTIFF creation
        kwargs = {
            'format': 'GTiff',
            'outputType': gdal.GDT_UInt16, # Maybe find anothre type it fit tou our data and take less space? 
            'creationOptions': ['COMPRESS=DEFLATE']
        }
        
        # Convert VRT to GeoTIFF
        gdal.Translate(output_path, vrt, **kwargs)
        
        print(f"GeoTIFF file created for {habitat} at: {output_path}")

print("Processing complete for all habitats.")