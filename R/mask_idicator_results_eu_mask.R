# Clean the environment
rm(list = ls())
gc()

# Import the libraries
library(terra)

## Before running check the paths and the names of the files ##
###############################################################

# Define the root folder
root <- "D:\\Emmanuel_Oceguera\\Fragmentation_analysis\\output\\EUNIS"
eu_mask <- "I:/biocon/Emmanuel_Oceguera/projects/Fragmentation_analysis/data/eu_mask_single.shp"
output_root <- "S:\\Emmanuel_OcegueraConchas\\fragmentation_analysis\\EUNIS"

# Define the years to process
year <- 2012  # Adjust this list based on available years

# Read the EU mask
eu_mask <- terra::vect(eu_mask)
#plot(eu_mask)
habitats_groups = c('N', 'Q', 'R', 'S', 'T', 'U', 'V')

# Loop over years
for (group in habitats_groups[2]) {
  cat("\nProcessing group:", group, "\n")
  
  # Define the raster file path
  group_dir <- file.path(root, as.character(year), group)
  
  if (!file.exists(group_dir)) {
    cat("Skipping year:", group, " - Folder does not exist.\n")
    next
  }

  for( habitat in list.files(group_dir)){
    # We want to skip Q24, Q25, Q41, Q42
    if (grepl("Q24|Q25|Q41|Q42", habitat)) {
      cat("Skipping habitat:", habitat, " - Not a valid habitat.\n")
      next
    }

    cat("processing:", habitat, "\n")
    habitat_dir <- file.path(group_dir, habitat)
    
    # If there is not tiff file in the folder, skip it
    if (length(list.files(habitat_dir, pattern = "\\.tiff$", full.names = T)) == 0) {
      cat("Skipping habitat:", habitat, " - No mosaic tif found.\n")
      next
    }

    # Get the file
    habitat_mosaic <- list.files(habitat_dir, pattern = "\\.tiff$", full.names = T)
    # Open the raster
    raster <- terra::rast(habitat_mosaic)
    # Mask the raster
    raster_masked <- terra::mask(raster, eu_mask)
    # Define the output path 
    output_folder <- file.path(output_root, year, group)
    # if does not exist, create it
    if (!dir.exists(output_folder)) {
      dir.create(output_folder, recursive = TRUE)
      cat("Created folder:", output_folder, "\n")
    }
    # create ouput name
    output_name <- file.path(output_folder, paste0(habitat,"_",year,"_connect_EU27.tiff"))
    cat("Output file:", output_name, "\n")
  
    # Write the raster
    terra::writeRaster(raster_masked, 
                       output_name, 
                       overwrite = TRUE, 
                       gdal = c("COMPRESS=NONE", "TFW=YES"),
                       datatype = 'INT1U')
    
    cat("Done processing:", basename(output_name), "\n")
    
  }
}
  