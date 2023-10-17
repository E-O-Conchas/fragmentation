# Remove all objects from the workspace (memory) of the R session
rm(list=ls())
gc()

# load the required packages
library(sf)
library(dplyr)
library(ggplot2)


# claculate effective mesh size for country
calculate_meff <- function(patch_shapefile_path, country_shapefile_path) {
  # Read the shapefiles
  forest_patches <- st_read(patch_shapefile_path)
  estonia <- st_read(country_shapefile_path)
  
  # Calculate patch areas in km^2
  patches_sizes_km2 <- forest_patches %>%
    mutate(area_km2 = as.numeric(st_area(forest_patches) / 1e6))
  
  # Calculate the total area of the country in km^2
  crty_total_km2 <- as.numeric(st_area(estonia) / 1e6)
  
  # Calculate the squared area of the patches and sum of squared areas
  patches_squared_km2 <- patches_sizes_km2$area_km2^2
  sum_patches_squared_km2 <- sum(patches_squared_km2)
  
  # Square the total area of the country
  crty_total_squared_km2 <- crty_total_km2^2
  
  # Calculate the meff using the formula
  estonia_meff_km2 <- crty_total_squared_km2 / sum_patches_squared_km2
  
  return(estonia_meff_km2)
}


# Path to the shp
forest_patches_path <-  "I:/biocon/Emmanuel_Oceguera/projects/2023_09_Fragmentation/outputs/estonia/frag_patches_stonia.shp"
estonia_path <- "I:/biocon/Emmanuel_Oceguera/projects/2023_09_Fragmentation/data/NUTS2021_v22_Estonia.shp"


# Example usage:
estonia_meff_result <- calculate_meff(forest_patches_path, estonia_path)
cat("Effective Mesh Size (meff) in square km^2:", estonia_meff_result, "\n")





