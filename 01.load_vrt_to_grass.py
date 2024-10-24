# This script is intended to be used within the GRASS GIS environment.

from grass.pygrass.modules import Module

# Path to your Tiff file
input_raster = "S:/Path_to_your_data_set/fragmentation/.tiff"

# Define the name of the output raster layer in GRASS GIS
output_raster = "raster_layer_name"

# Import the raster using r.in.gdal
Module("r.in.gdal", input=input_raster, output=output_raster, overwrite=True)


# Note: The other way to upload a raster is as follows 
 # 1. Click the File button on the toolbar. 
 # 2. Select Import Raster
 # 3. Simplified raster import with projection
 # 4. Select the raster file