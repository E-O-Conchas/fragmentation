import grass.script as gscript



# Use the GRASS overwrite environment variable to allow overwriting of existing data

gscript.use_temp_region()  # Ensures that the region changes are temporary



try:

    # Set the Region of Interest to match the raster map that is being used

    gscript.run_command('g.region', raster='test@PERMANENT')



    # Calculate Clumps

    gscript.run_command('r.clump', input='test@PERMANENT', output='test_clump', overwrite=True)



    # Specify the full path for the output report file

    report_output_path = 'S:/Emmanuel_OcegueraConchas/eu_fragmentation_forest/test.txt'



    # Generate a Report with Unique Area and Units and save it to the specified path

    gscript.run_command('r.report', map='test', units='me', flags='n', output=report_output_path, overwrite=True)



finally:

    # Release the temporary region to revert back to the user's default region settings

    gscript.del_temp_region()



# Note: The script assumes that 'eu_forest_frag@PERMANENT' and 'eu_forest_frag_clump' refer to the correct raster maps.

