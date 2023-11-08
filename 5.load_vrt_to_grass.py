from grass.pygrass.modules import Module



# Define the path to your VRT file

input_vrt = "S:/Emmanuel_OcegueraConchas/eu_fragmentation_forest/valid_tiles_test2.vrt"



# Define the name of the output raster layer in GRASS GIS

output_raster = "eu_forest_frag_test"



# Import the raster using r.in.gdal

Module("r.in.gdal", input=input_vrt, output=output_raster, overwrite=True)

