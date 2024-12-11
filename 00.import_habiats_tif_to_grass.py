# Script imporst the given habitats type into the GRASS GIS
# It is important that to run this script you need to have
# each of the habitats in their specific habitat folder

from grass.pygrass.modules import Module
import os

# Define the habitats folders
habitats = [
    "N51", "R31", "R34", "R42", 
    "R57", "S31", "S38", "S41", 
    "S42", "S93", "T13", "T22", 
    "T27", "T34"
]

# Base folder where the data is stored
input_base_path = "S:/Emmanuel_OcegueraConchas/fragmentation_maps_tiles_and_input/Input_layers/EUNIS"

# Define the year
year = 2018

# Loop through each habitat and import the corresponding raster
for habitat in habitats:
    # Define the name of the tif file
    tif_name = f"{habitat}_{year}_Frag2_Map.tif"
    input_raster = os.path.join(input_base_path, habitat, str(year), tif_name)
    output_raster = tif_name.replace('.tif', '')  # Remove the .tif extension for GRASS
    
    # Check if the file exists before trying to import
    if os.path.exists(input_raster):
        print(f"Processing {tif_name}")
        Module("r.in.gdal", input=input_raster, output=output_raster, overwrite=True)
        print(f"Finished processing {tif_name}")
    else:
        print(f"File not found: {input_raster}. Skipping...")

print("Finished processing all rasters.")
