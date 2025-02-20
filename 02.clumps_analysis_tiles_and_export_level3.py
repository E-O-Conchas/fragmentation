"""

This script processes fragmentation maps for various habitats under the level 3 of the EUNIS, generating clump maps, reports, and exporting them to GeoTiff format. It runs in a GRASS GIS environment, assuming the fragmentation maps and region settings are correctly set. The script performs the following tasks for each habitat:

1. Sets up the output directories.

2. Masks the fragmentation maps.

3. Generates clump maps.

4. Creates reports on unique areas and units.

5. Tiles and exports the clump maps to GeoTiff format.

6. Creates a 'READY.txt' file to indicate successful processing.

The script ensures that all temporary region changes are reverted at the end of the process.

"""

# Import libraries
import grass.script as gscript
import os


# Define the EUNIS habitat level 3 codes to process
hbaitat_level_3 = 'R'

# These are done
# "R31", "R34", "R42", "R57"
# Define the list of habitats to process
habitats = [
    "R11", "R12", "R13", "R14", "R15", "R16", "R17", "R18", "R19", "R1A", "R1B", "R1C",
    "R1D", "R1E", "R1F", "R1G", "R1H", "R1J", "R1K", "R1L", "R1M", "R1N", "R1P", "R1Q",
    "R1R", "R1S", "R21", "R22", "R23", "R24", "R32", "R33", "R35", "R36",
    "R37", "R41", "R43", "R44", "R45", "R51", "R52", "R53", "R54", "R55", "R56", "R61", 
    "R62", "R63", "R64", "R65", "R73"
]

# Example name of the raster habitat type
# Output_2018_R1D_map.tif
for habitat in habitats:
    print(f"Processing habitat: {habitat}")
    year = 2018

    # Define your paths 
    base_output_path = rf'S:\Emmanuel_OcegueraConchas\fragmentation_maps_tiles_and_input\EUNIS\{hbaitat_level_3}\{habitat}\{year}'
    # exple of output of the base_output_path
    
    # List of fragmentation map types with corresponding output subfolders and clump name prefixes
    #frag_map_types = [
    #    ('Baseline_Fragmentation', 'bfragmap_tiles_clumps_EUNIS'),
    #    ('Fragmentation1', 'bfragmap1_tiles_clumps_EUNIS'),
    #    ('Frag2', 'bfragmap2_tiles_clumps_EUNIS')
    #]
    frag_map_types = [
        ('Frag2', 'bfragmap2_tiles_clumps_EUNIS')]
    
    # Set up paths and ensure directories exist
    frag_maps_list = []
    for map_type, subfolder in frag_map_types:
        # Create the output path
        output_path = os.path.join(base_output_path, subfolder)
        # Create the output directory if it does not exist
        os.makedirs(output_path, exist_ok=True)
        # Define map name and clump name dynamically based on habitat, year, and map type
        map_name = f"Output_{year}_{habitat}_Map"
        # Define the clump name prefix
        clump_name = f"{habitat}_{year}_{subfolder.replace('tiles_clumps_EUNIS', 'clump')}"
        # Append map details to the list
        frag_maps_list.append((map_name, output_path, clump_name))
    try:
        gscript.use_temp_region()  # Ensures that the region changes are temporary
        for map_name, output_path, clump_prefix in frag_maps_list:
            print(f"Processing {map_name}...")
            # Set region based on the map
            gscript.run_command('g.region', raster=map_name)
            # Mask the 0 values for each fragmentation map
            gscript.run_command('r.mask', raster=map_name, maskcats='1', overwrite=True)

            # Change the output name for the clump map to something like this 'T1B_bfragmap1_clump'
            clum_map_name = map_name.replace('Output', 'bfragmap').replace('_Map', '_clump')
            print(f"Clump map will be named: {clum_map_name}")
            gscript.run_command('r.clump', input=map_name, output=clum_map_name, overwrite=True)
            
            # Generate report
            report_output_path = os.path.join(output_path, 'report_unique_areas_and_units.ini')
            print(f"Generating report at: {report_output_path}")
            gscript.run_command('r.report', map=clum_map_name, units='me', flags='n', output=report_output_path, overwrite=True)

            # Riling and exporting
            print(f"Tiling and exporting clump map: {clum_map_name}")
            gscript.run_command('g.region', raster=f"{clum_map_name}@PERMANENT")
            gscript.run_command('r.tile', input=f"{clum_map_name}@PERMANENT", output=clump_prefix, width=1000, height=1000)

            # List tiles and export to GeoTiff format
            tiles = gscript.read_command('g.list', type='raster', pattern=f'{clump_prefix}*', mapset='PERMANENT').strip().splitlines()
            for tile in tiles:
                # Set the region to match the current tile
                gscript.run_command('g.region', raster=tile)
                output_file = os.path.join(output_path, f"{tile}.tif")
                print(f"Exporting {tile} to {output_file}")
                gscript.run_command('r.out.gdal', flags='c', input=tile, output=output_file, format='GTiff', nodata=0, type='Int32', overwrite=True, createopt="COMPRESS=DEFLATE")
            
            # Create a flag file to indicate that the process was successful
            ready_flag_path = os.path.join(output_path, 'READY.txt')
            with open(ready_flag_path, 'w') as f:
                f.write("Preprocessing complete. Folder is ready for fragmentation analysis.")
            print(f"Ready flag created at {ready_flag_path}")

            # Remove the mask for the next iteration
            gscript.run_command('r.mask', flags='r')

        print("All fragmentation maps have been processed and exported successfully.")
        
    except gscript.ScriptError as e:
        print(f"An error occurred: {e}")
        
    finally:
        # Restore original region settings
        gscript.del_temp_region()
        print("Temporary region reset to default.")

print("All habitats have been processed successfully.")


