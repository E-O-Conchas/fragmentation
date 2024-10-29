# Clean the environment
rm(list = ls())
gc()


library(terra)
library(here)

here(root)

root <- "S:\\Emmanuel_OcegueraConchas\\fragmentation_analysis"

list <- c(base = "base_fragmnetation_map",
          map_1 = 1,
          map_2 = 2)



list[[1]]

for ( m in list ){
  print(m)
  
}

# Create the link to the data 


path <- file.path(here(root, base))



# Output VRT file path
vrt_path = "S:\\Emmanuel_OcegueraConchas\\fragmentation_analysis\\EUNIS\\00_version_100m\\base_fragmentation_map2_EUNIS\\bfragmap2_meff_EUNIS\\window_count3.vrt"
eu_mask = "I:/biocon/Emmanuel_Oceguera/projects/Fragmentation_analysis/data/eu_mask_single.shp"

# Read the mask
eu_mask <- terra::vect(eu_mask)

# Read raster
raster <- terra::rast(vrt_path)
plot(raster)

# mask raster
raster_masked <- terra::mask(raster, eu_mask)

# Plot it
plot(raster_masked)

# Write the raster
output_name <- "S:\\Emmanuel_OcegueraConchas\\fragmentation_analysis\\EUNIS\\00_version_100m\\base_fragmentation_map2_EUNIS\\tiff\\bfragmap2_meff_eunis_masked.tif"
terra::writeRaster(raster_masked, output_name,overwrite = F, gdal=c("COMPRESS=NONE", "TFW=YES"), datatype='INT1U')
