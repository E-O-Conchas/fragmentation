#!/usr/bin/env python3

import os
import grass.script as gscript

# Set region to match the raster
gscript.run_command('g.region', raster='frag_unique_masked@PERMANENT')


# Tile the raster
gscript.run_command('r.tile', input='frag_unique_masked@PERMANENT', output='name_tile', width=20000, height=20000)


# Define the path to the output directory
output_dir = r"I:\biocon\Emmanuel_Oceguera\projects\2023_09_Fragmentation\estonia_forest_fragmentation\result_grass\tiles_clump_masked"

# Get a list of all tiles that start with 'tile_test*'
tiles = gscript.read_command('g.list', type='raster', pattern='name_tile*', mapset='PERMANENT').strip().splitlines()

# Export each tile to a GeoTIFF file
for tile in tiles:
    # Set region to match the raster before exporting__
    gscript.run_command('g.region', raster=tile)
    # Define the output file path
    output_file = os.path.join(output_dir, f"{tile}.tif")
    # Export the tile using r.out.gdal
    print(f"Exporting {tile} to {output_file}")
    result = gscript.run_command('r.out.gdal', flags='c', input=tile, output=output_file, format='GTiff', nodata=0, type='Int32', overwrite=True, createopt="COMPRESS=DEFLATE")
    
    if result != 0:
        print(f"Failed to export {tile}.")
    else:
        print(f"Successfully exported {tile}.")
