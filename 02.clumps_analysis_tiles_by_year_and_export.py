"""
This script processes fragmentation maps by year, based on the structure:
I:/path_to_your_input_folder/
    ├── 2000/
    │     └── Fragmentation_2000.tif
    ├── 2005/
    │     └── Fragmentation_2005.tif
    ├── 2010/
    │     └── Fragmentation_2010.tif
    ├── 2015/
    │     └── Fragmentation_2015.tif
    └── 2020/
          └── Fragmentation_2020.tif
"""

# Import libraries
import grass.script as gscript
import os

# Define the years available in the folder structure
years = ["2000", "2005", "2010", "2015", "2020"]

# Base path for input and output
base_path = "I:/Emmanuel_Oceguera/projects/fragmentation/input"
output_path = r"I:\Emmanuel_Oceguera\projects\fragmentation\output"

# Loop through each year
for year in years:
    print(f"Processing year: {year}")
    
    # Define paths for the current year
    year_input_path = os.path.join(base_path, year, f"Fragmentation_{year}.tif")
    year_output_path = os.path.join(output_path , year, "tiles")  # Output folder for each year
    os.makedirs(year_output_path, exist_ok=True)

    # Check if the input file exists
    if not os.path.exists(year_input_path):
        print(f"File not found: {year_input_path}. Skipping...")
        continue

    # Define map names
    map_name = f"Fragmentation_{year}"
    clump_map_name = f"Fragmentation_{year}_clump"

    try:
        gscript.use_temp_region()  # Ensures that the region changes are temporary
        
        # Import the raster into GRASS # This step is not needed if the raster is already in the GRASS database	
        # print(f"Importing raster: {year_input_path}")
        # gscript.run_command('r.in.gdal', input=year_input_path, output=map_name, overwrite=True)

        # Set the region based on the map
        gscript.run_command('g.region', raster=map_name)

        # Mask the 0 values for each fragmentation map
        gscript.run_command('r.mask', raster=map_name, maskcats='1', overwrite=True)

        # Generate clump map
        print(f"Generating clump map: {clump_map_name}")
        gscript.run_command('r.clump', input=map_name, output=clump_map_name, overwrite=True)

        # Generate report
        report_output_path = os.path.join(year_output_path, 'report_unique_areas_and_units.ini')
        print(f"Generating report at: {report_output_path}")
        gscript.run_command('r.report', map=clump_map_name, units='me', flags='n', output=report_output_path, overwrite=True)

        # Tiling and exporting clump map
        print(f"Tiling and exporting clump map: {clump_map_name}")
        gscript.run_command('g.region', raster=f"{clump_map_name}@PERMANENT")
        tile_prefix = f"frag_{year}_tile"
        gscript.run_command('r.tile', input=f"{clump_map_name}@PERMANENT", output=tile_prefix, width=1000, height=1000)

        # List tiles and export to GeoTiff format
        tiles = gscript.read_command('g.list', type='raster', pattern=f'{tile_prefix}*', mapset='PERMANENT').strip().splitlines()
        for tile in tiles:
            # Set the region to match the current tile
            gscript.run_command('g.region', raster=tile)
            output_file = os.path.join(year_output_path, f"{tile}.tif")
            print(f"Exporting {tile} to {output_file}")
            gscript.run_command('r.out.gdal', flags='c', input=tile, output=output_file, format='GTiff', nodata=0, type='Int32', overwrite=True, createopt="COMPRESS=DEFLATE")
        
        # Create a flag file to indicate that the process was successful
        ready_flag_path = os.path.join(year_output_path, 'READY.txt')
        with open(ready_flag_path, 'w') as f:
            f.write("Preprocessing complete. Folder is ready for fragmentation analysis.")
        print(f"Ready flag created at {ready_flag_path}")

        # Remove the mask for the next iteration
        gscript.run_command('r.mask', flags='r')

        print(f"Processing complete for year {year}")

    except gscript.ScriptError as e:
        print(f"An error occurred while processing year {year}: {e}")
        
    finally:
        # Restore original region settings
        gscript.del_temp_region()
        print("Temporary region reset to default.")

print("All years have been processed successfully.")
