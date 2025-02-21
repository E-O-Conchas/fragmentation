# Clean the environment
rm(list = ls())
gc()

# Import the libraries
library(terra)

## Before running check the paths and the names of the files ##
###############################################################

# Set the tem dir to avoid large use of ram memory
terraOptions(memmax = 1, todisk=TRUE, tempdir = "E:\\Emmanuel\\fragmentation\\tem")

# Define the root folder
root <- "S:\\user_name\\fragmentation_analysis\\EUNIS\\R"
eu_mask <- "I:/biocon/user_name/projects/Fragmentation_analysis/data/eu_mask_single.shp"

# Define the habitats
habitats <- c("R12", "R13", "R14", "R15", "R16", "R17", "R18", "R19", "R1A", "R1B", "R1C",
              "R1D", "R1E", "R1F", "R1G", "R1H", "R1J", "R1K", "R1L", "R1M", "R1N", "R1P", "R1Q",
              "R1R", "R1S", "R21", "R22", "R23", "R24", "R32", "R33", "R35", "R36", "R37", "R41", 
              "R43", "R44", "R45", "R52", "R53", "R54", "R55", "R56", "R61", "R62", "R63", "R64", 
              "R65", "R73")
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
  cat("Processing habitat: ", habitat, "\n")
  for (map_type in map_types[3]) { # only the base fragmentation map 2 this time
    # Define the path where the data is stored
    folder <- file.path(root, habitat,year, map_type)
    # we list the unique raster file in the folder
    raster_file <- list.files(folder, pattern = '.tif$', full.names = TRUE)
    #print(raster_file)
    # Read the raster
    cat("Processing: ", basename(raster_file), "\n")
    raster <- terra::rast(raster_file)

    # Mask te raster using the EU mask
    raster_masked <- terra::mask(raster, eu_mask)

    # Define the output path
    output_folder <- file.path(folder, 'tiff')
    # Create output directory if it doesn't exist
    if (!dir.exists(output_folder)) dir.create(output_folder)
    
    output_name <- file.path(output_folder, paste0(sub('\\..*$', '', basename(raster_file)),'_EU27.tiff'))
    cat("Output file: ", basename(output_name), "\n")	
    # write the raster
    terra::writeRaster(raster_masked, output_name,overwrite = F, gdal=c("COMPRESS=NONE", "TFW=YES"), datatype='INT1U')
    cat("Raster saved................:)\n")
  }
}

message("All done")
