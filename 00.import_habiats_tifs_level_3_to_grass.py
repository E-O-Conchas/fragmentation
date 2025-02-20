# this script is designed to import all .tif files in a folder 
# that represent the EUNIS habitats level 3 from the European Environment Agency
# The script is designed to be run in the GRASS GIS Python environment.

# Import the GRASS GIS Python API
from grass.pygrass.modules import Module
import os

# Define the EUNIS habitats level 3 to import
habitats = ["R"]  # You can list other habitat folders if needed, e.g., ["N", "T", ...]

# Base folder where the data is stored
input_base_path = r"I:\biocon\Nikolaj_Poulsen\Fragmentation_project\EUNIS Habitats\Fragmentations maps"

# Define the year
year = 2018

# Loop through each habitat
for habitat in habitats:
    habitat_path = os.path.join(input_base_path, str(year),habitat)
    print(habitat_path)
    # Check if the habitat path exists
    if os.path.exists(habitat_path):
        # Loop through each .tif file in the habitat folder
        for tif_file in os.listdir(habitat_path):
            if tif_file.endswith('.tif'):  # Only process .tif files
                input_raster = os.path.join(habitat_path, tif_file)
                output_raster = tif_file.replace('.tif', '')  # Remove the .tif extension for GRASS
                
                # Check if the file exists before importing
                if os.path.exists(input_raster):
                    print(f"Processing {tif_file}")
                    Module("r.in.gdal", input=input_raster, output=output_raster, overwrite=True)
                    print(f"Finished processing {tif_file}")
                else:
                    print(f"File not found: {input_raster}. Skipping...")
    else:
        print(f"Habitat folder not found: {habitat_path}. Skipping...")

print("Finished processing all rasters.")