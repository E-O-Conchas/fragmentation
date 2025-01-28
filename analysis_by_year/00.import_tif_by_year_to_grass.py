
# Import the GRASS GIS Python API
from grass.pygrass.modules import Module
import os

# Base folder where the data is stored
input_base_path = "I:/biocon/Emmanuel_Oceguera/projects/WildE_magali/fragmentation/input"

# Define the years available in the folder structure
years = ["2000", "2006", "2012", "2018"]

# Loop through each year folder
for year in years:
    # Define the path to the year's folder
    year_folder = os.path.join(input_base_path, year)
    
    # Define the name of the raster file for the current year
    tif_name = f"Fragmentation_{year}.tif"
    input_raster = os.path.join(year_folder, tif_name)
    output_raster = tif_name.replace('.tif', '')  # Remove the .tif extension for GRASS
    
    # Check if the file exists before trying to import
    if os.path.exists(input_raster):
        print(f"Processing {tif_name} for year {year}")
        Module("r.in.gdal", input=input_raster, output=output_raster, overwrite=True)
        print(f"Finished processing {tif_name} for year {year}")
    else:
        print(f"File not found: {input_raster}. Skipping...")

print("Finished processing all rasters.")
