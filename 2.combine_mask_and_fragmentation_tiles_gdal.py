import os
from glob import glob
import numpy as np
import re
from osgeo import gdal
from multiprocessing import Pool

# Define file paths for fragmentation and land rasters
frag_path = r"S:\Emmanuel_OcegueraConchas\eu_fragmentation_forest\frag_raster"
land_path = r"S:\Emmanuel_OcegueraConchas\eu_fragmentation_forest\land_raster"
out_path = r"S:\Emmanuel_OcegueraConchas\eu_fragmentation_forest\frag_land_combined"

# Define a regular expression pattern to match tile filenames
pattern = r'frag_tile_x(\d+)_y(\d+)_1.tif'

# Get a list of tile filenames from the fragmentation raster folder
tiles = []
for file_path in glob(frag_path + os.sep + '*.tif'):
    match = re.search(pattern, file_path)
    if match:
        x_tile = match.group(1)
        y_tile = match.group(2)
        tiles.append(f"x{x_tile}_y{y_tile}_1.tif")
    else:
        print(f"Skipping file: {file_path}")

# Initialize GDAL
gdal.AllRegister()

def process_tile(t):
    # Define the file paths for the current tile's fragmentation and land rasters
    frag_p = os.path.join(frag_path, 'frag_tile_' + t)
    land_p = os.path.join(land_path, 'mask_tile_' + t)

    # Open the fragmentation and land rasters using GDAL
    frag_ds = gdal.Open(frag_p)
    land_ds = gdal.Open(land_p)

    # Get the band objects
    frag_band = frag_ds.GetRasterBand(1)
    land_band = land_ds.GetRasterBand(1)

    # Read the raster data as numpy arrays
    frag_data = frag_band.ReadAsArray()
    land_data = land_band.ReadAsArray()

    # Combine the two rasters
    out_data = np.where((frag_data == 9) & (land_data == 1), 9, land_data)

    # Create the output raster
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(
        os.path.join(out_path, 'lf_comb_' + t),
        frag_ds.RasterXSize,
        frag_ds.RasterYSize,
        1,
        gdal.GDT_Byte,
        ['COMPRESS=DEFLATE']
    )

    # Set the projection and geotransform
    out_ds.SetProjection('EPSG:3035')
    out_ds.SetGeoTransform(frag_ds.GetGeoTransform())

    # Write the output data
    out_band = out_ds.GetRasterBand(1)
    out_band.SetNoDataValue(0)
    out_band.WriteArray(out_data)

    # Close the datasets
    out_band = None
    out_ds = None
    frag_ds = None
    land_ds = None

# Process the tiles using multiprocessing to utilize multiple cores
if __name__ == '__main__':
    with Pool(processes=os.cpu_count()) as pool:
        pool.map(process_tile, tiles)











