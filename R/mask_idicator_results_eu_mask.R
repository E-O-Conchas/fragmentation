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




#### We parallelize the code ####
# We use the future package to parallelize the code
# It works with the future.apply package and the terra package
# It is way faster than the previous code

# Clean the environment
rm(list = ls())
gc()

# Load libraries
library(terra)
library(future.apply)

# Parallel setup
plan(multisession, workers = 4)  # Adjust number of workers based on your system

# Define paths
root <- "D:\\Emmanuel_Oceguera\\Fragmentation_analysis\\output\\EUNIS"
eu_mask_path <- "I:/biocon/Emmanuel_Oceguera/projects/Fragmentation_analysis/data/eu_mask_single.shp"
output_root <- "S:\\Emmanuel_OcegueraConchas\\fragmentation_analysis\\test"
year <- 2012
#eu_mask <- terra::vect(eu_mask_path)
habitats_groups <- c('N', 'Q', 'R', 'S', 'T', 'U', 'V')

# Loop over groups (sequentially, but can also be parallelized)
for (group in habitats_groups[2]) {
  cat("\nProcessing group:", group, "\n")
  group_dir <- file.path(root, as.character(year), group)
  
  if (!file.exists(group_dir)) {
    cat("Skipping group:", group, " - Folder does not exist.\n")
    next
  }
  
  habitats <- list.files(group_dir)
  
  future_lapply(habitats, function(habitat) {
    cat("Processing:", habitat, "\n")
    habitat_dir <- file.path(group_dir, habitat)
    
    # Skip if no TIFF
    tiff_files <- list.files(habitat_dir, pattern = "\\.tiff$", full.names = TRUE)
    if (length(tiff_files) == 0) {
      cat("Skipping habitat:", habitat, " - No mosaic tif found.\n")
      return(NULL)
    }
    
    raster <- terra::rast(tiff_files)
    eu_mask <- terra::vect(eu_mask_path)
    raster_masked <- terra::mask(raster, eu_mask)
    
    output_folder <- file.path(output_root, year, group)
    if (!dir.exists(output_folder)) {
      dir.create(output_folder, recursive = TRUE)
      cat("Created folder:", output_folder, "\n")
    }
    
    output_name <- file.path(output_folder, paste0(habitat, "_", year, "_connect_EU27.tiff"))
    cat("Writing to:", output_name, "\n")
    
    terra::writeRaster(
      raster_masked,
      output_name,
      overwrite = TRUE,
      gdal = c("COMPRESS=NONE", "TFW=YES"),
      datatype = 'INT1U'
    )
    
    cat("Done processing:", basename(output_name), "\n")
    return(output_name)
  })
}
