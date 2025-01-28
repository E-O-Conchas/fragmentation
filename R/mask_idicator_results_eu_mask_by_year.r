# Clean the environment
rm(list = ls())
gc()

# Import the libraries
library(terra)

## Before running check the paths and the names of the files ##
###############################################################

# Define the root folder
root <- "I:\\biocon\\Emmanuel_Oceguera\\projects\\WildE_magali\\fragmentation\\output"
eu_mask <- "I:/biocon/Emmanuel_Oceguera/projects/Fragmentation_analysis/data/eu_mask_single.shp"

# Define the years to process
years <- c(2000, 2006, 2012, 2018)  # Adjust this list based on available years
years <- c(2006)
# Read the EU mask
eu_mask <- terra::vect(eu_mask)
#plot(eu_mask)

# Loop over years
for (year in years) {
  cat("\nProcessing year:", year, "\n")

  # Define the raster file path
  raster_path <- file.path(root, as.character(year), "meff_calculation", paste0("frag_meff_", year, ".tif"))
  
  if (!file.exists(raster_path)) {
    cat("Skipping year:", year, " - Folder does not exist.\n")
    next
  }
  cat("Processing:", raster_path, "\n")
  
  # Read the raster
  raster <- terra::rast(raster_path)
  # Mask the raster
  raster_masked <- terra::mask(raster, eu_mask)
  # Define the output path 
  output_name <- file.path(root, year, "meff_calculation" , paste0("frag_meff_", year, "_EU27.tiff"))
  cat("Output file:", output_name, "\n")
  
  # Write the raster
  terra::writeRaster(raster_masked, output_name, overwrite = TRUE, 
                     gdal = c("COMPRESS=NONE", "TFW=YES"), datatype = 'INT1U')
  
  cat("Done processing:", raster_path, "\n")
}
message("All done!")
