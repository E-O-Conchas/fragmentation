#######################################################################
# Author: Emmanuel Oceguera-Conchas, Nikolaij
# Work: Import multiple TIFF files into GRASS GIS
#
# Note: This script is intended to be used within the GRASS GIS environment.
#######################################################################

# Import libraries
import os
from glob import glob
from grass.pygrass.modules import Module

# Input folder
input_raster = "S:/Path_to_your_data_set/fragmentation"

# Define a function to import all TIFF files in the folder
def import_tiff_from_folders(folders, overwrite=True):
    '''
    Imports all TIFF files from a list of folders into GRASS GIS.

    parameters:
    Folder(list): List of folder paths containing the TIFF files.
    overwrite(bool): whether to evrwrite existing layers in GRASS GIS.

    '''
    for folder in folders:

        # Find all the TIFF in the current folder
        tiff_files = glob(os.path.join(folder, "*.tiff"))

        if not tiff_files:
            print(f"No TIFF files found in {folder}.")
            continue

        for tiff_file in tiff_files:

            # Define the output raster name based on the file name
            output_raster = os.path.basename(tiff_file).replace('.tif', '')

            # Import raster using r.in.gdal
            print(f"Importing {tiff_file} as {output_raster}...")
            Module("r.in.gdal", input=tiff_file, output=output_raster, overwrite=overwrite)
            print(f"Imported {tiff_file} successfully.")


# List of folders containing TIFF files
folders = [
    "S:/Path_to_your_data_set/fragmentation",
    "S:/Path_to_your_data_set/fragmentation",
    "S:/Path_to_your_data_set/fragmentation",
]

# Call the function
import_tiff_from_folders(folders)

# Note: The other way to upload a raster is as follows 
 # 1. Click the File button on the toolbar. 
 # 2. Select Import Raster
 # 3. Simplified raster import with projection
 # 4. Select the raster file
