import grass.script as gscript
import os

# Define your paths correctly, using double backslashes in Windows paths
base_output_path = r'S:\Emmanuel_OcegueraConchas\fragmentation_analysis\EUNIS\T1B\2000'

# Ensure that both output directories exist
fragmap_output_path = os.path.join(base_output_path, 'bfragmap_tiles_clumps_EUNIS')
fragmap1_output_path = os.path.join(base_output_path, 'bfragmap1_tiles_clumps_EUNIS')
fragmap2_output_path = os.path.join(base_output_path, 'bfragmap2_tiles_clumps_EUNIS')

if not os.path.exists(fragmap_output_path):
    os.makedirs(fragmap_output_path)

if not os.path.exists(fragmap1_output_path):
    os.makedirs(fragmap1_output_path)

if not os.path.exists(fragmap2_output_path):
    os.makedirs(fragmap2_output_path)

# List of T1B fragmentation maps and their corresponding output directories
frag_maps_list = [
    ('T1B_2000_Baseline_Fragmentation_Map', fragmap_output_path, 'T1B_2000_bfragmap_clump'),
    ('T1B_2000_Fragmentation1_Map', fragmap1_output_path, 'T1B_2000_bfragmap1_clump'),
    ('T1B_2000_Fragmentation2_Map', fragmap2_output_path, 'T1B_2000_bfragmap2_clump')
]

try:
    gscript.use_temp_region()  # Ensures that the region changes are temporary

    for frag_map, output_path, tile_prefix in frag_maps_list:
        print(f"Processing {frag_map}...")

        # Set the Region of Interest to match the raster map that is being used
        gscript.run_command('g.region', raster=frag_map)

        # Before running the clumps we run the r.mask to mask the 0 values for each fragmentation map
        gscript.run_command('r.mask', raster=frag_map, maskcats='1', overwrite=True)

        # Change the output name for the clump map to something like this 'T1B_bfragmap1_clump'
        frag_map_name = frag_map.replace('Fragmentation', 'bfragmap').replace('_Map', '_clump')
        print(f"Clump map will be named: {frag_map_name}")
        # This will result in 'T1B_bfragmap1_clump' for the first map and 'T1B_bfragmap2_clump' for the second map
        # Calculate Clumps
        gscript.run_command('r.clump', input=frag_map, output=frag_map_name, overwrite=True)
        
        # Define path for report output in the correct directory
        report_output_path = os.path.join(output_path, 'report_unique_areas_and_units.ini')
        print(f"Generating report at: {report_output_path}")

        # Generate a Report with Unique Area and Units and save it to the specified path
        gscript.run_command('r.report', map=frag_map_name, units='me', flags='n', output=report_output_path, overwrite=True)

        # --- Start of Tiling and Exporting Process ---
        print(f"Tiling and exporting clump map: {frag_map_name}")

        # Set the region to match the clump map
        gscript.run_command('g.region', raster=f"{frag_map_name}@PERMANENT")

        # Tile the clump map
        gscript.run_command('r.tile', input=f"{frag_map_name}@PERMANENT", output=tile_prefix, width=1000, height=1000)

        # Get a list of all generated tiles
        tiles = gscript.read_command('g.list', type='raster', pattern=f'{tile_prefix}*', mapset='PERMANENT').strip().splitlines()

        # Export each tile to GeoTIFF format
        for tile in tiles:
            # Set the region to match the current tile
            gscript.run_command('g.region', raster=tile)

            # Define the output file path for each tile
            output_file = os.path.join(output_path, f"{tile}.tif")

            # Export the tile using r.out.gdal
            print(f"Exporting {tile} to {output_file}")
            gscript.run_command('r.out.gdal', flags='c', input=tile, output=output_file, format='GTiff', nodata=0, type='Int32', overwrite=True, createopt="COMPRESS=DEFLATE")
        
        # Remove the mask for the next iteration
        gscript.run_command('r.mask', flags='r')

    print("All fragmentation maps have been processed and exported successfully.")
    
except gscript.ScriptError as e:
    print(f"An error occurred: {e}")
    
finally:
    # Restore original region settings
    gscript.del_temp_region()
    print("Temporary region reset to default.")

print("Processing complete.")