# Clean the environment
rm(list = ls())
gc()

# Import the libraries
library(terra)

# Define the root folder
root <- "S:\\Emmanuel_OcegueraConchas\\fragmentation_analysis\\EUNIS"
eu_mask <- "I:/biocon/Emmanuel_Oceguera/projects/Fragmentation_analysis/data/eu_mask_single.shp"
# 
# Define the habitats
habitats <- c("R42", "R57", "S31",
              "S38", "S41", "S42", "S93", "T13", "T22", "T27", "T34")

# habitats <- c("R34")

# Define the year
year <- 2018

# Define  te map types
map_types <- c("base_fragmentation_map_EUNIS/bfragmap_meff_EUNIS",
               "base_fragmentation_map1_EUNIS/bfragmap1_meff_EUNIS",
               "base_fragmentation_map2_EUNIS/bfragmap2_meff_EUNIS")

# read the mask
eu_mask <- terra::vect(eu_mask)

# Loop over the habitats and the map types
for (habitat in habitats) {
  for (map_type in map_types[3]) { # only the base fragmentation map 2 this time
    # Define the path where the data is stored
    folder <- file.path(root, habitat,year, map_type)
    # we list the unique raster file in the folder
    raster_file <- list.files(folder, pattern = '.tif$', full.names = TRUE)
    print(raster_file)
    # Read the raster
    message("Processing: ", raster_file)
    raster <- terra::rast(raster_file)

    # Mask te raster using the EU mask
    raster_masked <- terra::mask(raster, eu_mask)

    # Define the output path
    output_folder <- file.path(folder, 'tiff')
    # Create output directory if it doesn't exist
    if (!dir.exists(output_folder)) dir.create(output_folder)
    
    output_name <- file.path(output_folder, paste0(sub('\\..*$', '', basename(raster_file)),'_Eu27.tiff'))
    print(output_name)
    # write the raster
    terra::writeRaster(raster_masked, output_name,overwrite = F, gdal=c("COMPRESS=NONE", "TFW=YES"), datatype='INT1U')

    message("Masked raster saved in: ", output_name)

  }
}

message("All done")