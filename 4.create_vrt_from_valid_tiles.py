# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 16:43:30 2023

@author: no67wuwu

work: create the vrt from the valid tiles that has been created in the step 4 

"""

from osgeo import gdal

# Define the paths
input_txt_file = r"S:\Emmanuel_OcegueraConchas\fragmentation_estonia_test\valid_tiles.txt" # Replace with the path to your text file
output_vrt_file = r"S:\Emmanuel_OcegueraConchas\fragmentation_estonia_test\valid_tiles.vrt"     # Replace with the desired VRT file path

# Read the list of image file paths from the text file
with open(input_txt_file, "r") as file:
    image_paths = [line.strip() for line in file]

# Create a VRT dataset
vrt_options = gdal.BuildVRTOptions(resolution="highest")
vrt_dataset = gdal.BuildVRT(output_vrt_file, image_paths, options=vrt_options)

# Optionally, set additional VRT properties
vrt_dataset.SetMetadata({"fragmentation land and mask titles": "Merged VRT", "Description": "Generated VRT from a list of files that have been created in the step 4"})

# Close the VRT dataset
vrt_dataset = None

print(f"VRT file '{output_vrt_file}' has been created.")
