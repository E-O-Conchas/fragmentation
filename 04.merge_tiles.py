# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 19:40:05 2024

@author: no67wuwu
Work: This script takes all the tifles from the results folder 
        and convert it to a vrt file and tiff files as output.
"""

import rasterio
from rasterio.mask import mask
from rasterio.merge import merge
import os
import glob

def merge_tiles(tiles, output_path):
    """
    Merge multiple tiles into a single GeoTIFF.

    Parameters:
    tiles (list): List of paths to tile GeoTIFF files.
    output_path (str): Path for the output merged GeoTIFF.
    """
    if not tiles:
        print("No tiles to merge.")
        return
    
    # Open all tile files
    tile_datasets = [rasterio.open(tile) for tile in tiles]
    
    # Merge the tiles
    mosaic, transform = merge(tile_datasets)
    
    # Get the metadata of the first tile to set for the output file
    out_meta = tile_datasets[0].meta.copy()
    out_meta.update({
        "driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": transform,
        "compress": "deflate"
    })

    # Ensure that the output path exists
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    # Write the merged mosaic to a new GeoTIFF
    with rasterio.open(output_path, "w", **out_meta) as dest:
        dest.write(mosaic)

    # Close all tile datasets
    for ds in tile_datasets:
        ds.close()

    print(f"Merged file saved as: {output_path}")

##############################################################################
####### Run the merge_tiles function for each habitat and year ###############
##############################################################################

# Define the directory name
base_dir = r'S:\Emmanuel_OcegueraConchas\fragmentation_analysis\EUNIS'
# Define the habitats 
habitats = [ "N51", "R31", "R34", "R42", 
            "R57", "S31", "S38", "S41", 
            "S42", "S93", "T13", "T22", 
            "T27", "T34"]
# Define the year
year = 2018

# Define all fragmentation maps and corresponding meff folders
map_folders = [
    ("base_fragmentation_map2_EUNIS", "bfragmap2_meff_EUNIS"),]

# ("base_fragmentation_map_EUNIS", "bfragmap_meff_EUNIS"),
#     ("base_fragmentation_map1_EUNIS", "bfragmap1_meff_EUNIS"),

# Define the subfolder containing the tiles
window_count_folder = "window_count3"

for habitat in habitats:
    print(f"Processing habitat: {habitat}")
    
    for map_folder, meff_folder in map_folders:
        print(f"Processing map: {map_folder}")

        # Define the input path for tiles
        input_path = os.path.join(base_dir, habitat, str(year), map_folder, meff_folder, window_count_folder)
        tiles = glob.glob(os.path.join(input_path, "*.tif"))

        if not tiles:
            print("No tiles found.")
            continue
        
        map_type = meff_folder
        merged_file_name = f"{habitat}_{map_type}_merged.tif"
        # Define the output path for the merged file
        output_folder = os.path.join(base_dir, habitat, str(year), map_folder)
        output_path = os.path.join(output_folder, merged_file_name)
        print(output_path)
        merge_tiles(tiles, output_path)

print("All tiles for all selected habitats and years have been merged.")


### Test the merge_tiles function
r"S:\Emmanuel_OcegueraConchas\fragmentation_analysis\EUNIS\R51\2018\base_fragmentation_map_EUNIS\bfragmap_meff_EUNIS\window_count3"
out_path = r"S:\Emmanuel_OcegueraConchas\fragmentation_analysis\EUNIS\R51\2018\base_fragmentation_map_EUNIS\bfragmap_meff_EUNIS"
# List all .tif files in the folder
tiles = glob.glob(os.path.join(path, "*.tif"))
# Define the output file path for the merged file
merged_output_file = os.path.join(out_path, "bfragmap_meff_eunis.tif")
# Call merge_tiles to merge the tiles
merge_tiles(tiles, merged_output_file)



