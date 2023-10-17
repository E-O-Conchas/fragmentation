# Remove all objects from the workspace (memory) of the R session
rm(list=ls())
gc()

# load the required packages
library(sf)
library(dplyr)

setwd("C:/Emmanuel_Oceguera_LocalW10sys/Evirionment_R")

# Effective mesh size  
# meff = (Atotal^2) / Σ(Ai^2)

# Path to the shp
forest_patches_path <-  "I:/biocon/Emmanuel_Oceguera/projects/2023_09_Fragmentation/outputs/estonia/frag_patches_stonia.shp"
estonia_path <- "I:/biocon/Emmanuel_Oceguera/projects/2023_09_Fragmentation/data/NUTS2021_v22_Estonia.shp"

# Open files
forest_patches <- st_read(forest_patches_path)
estonia <- st_read(estonia_path)

# Effective mesh size equation 
# meff = (Atotal^2) / Σ(Ai^2)

# Define the sizes of the patches km²
patches_sizes_km2 <- forest_patches %>% 
  mutate(area_km2 = as.numeric(st_area(forest_patches)/1e6))

# Define the total area of the country
crty_total_km2 <- as.numeric(st_area(estonia)/1e6)

# Calculate the squared area of the patches and sum of squered 
patches_squared_km2 <- patches_sizes_km2$area_km2**2
sum_patches_squared_km2 <- sum(patches_squared_km2)

# Squared the total area of the country
crty_total_squared_km2 <- crty_total_km2**2

# calculate the meff using the formula
estonia_meff_km2 <- crty_total_squared_km2/sum_patches_squared_km2

# Merge meff values with the forest_patches data
forest_patches_meff <- cbind(forest_patches, meff = estonia_meff_km2)

# Print the result
cat("Effective Mesh Size (meff) in square km^2:", estonia_meff_km2, "/n")

# Result 
"Effective Mesh Size (meff) in square km^2: 12017.86"


# Visualization of the mesh size in Estonia
# Create a ggplot object for the map
ggplot() +
  geom_sf(data = estonia, fill = "lightgray") +
  geom_sf(data = forest_patches_meff, aes(fill = meff), color = NA) +
  coord_sf(crs= 3035) +
  scale_fill_gradient(low = "green", high = "red") +
  theme_bw(base_line_size = NA) +
  labs(title = "Effective Mesh Size (meff) Map for old grow Forest Patches in Estonia")



# Save the result
output_path <- "I:/biocon/Emmanuel_Oceguera/projects/2023_09_Fragmentation/outputs/estonia"
file_name <- paste0(output_path,"/", "estonia_meffkm2.shp")
st_write(forest_patches_meff, file_name, driver = "ESRI Shapefile", overwrite= TRUE)



# # Create a choropleth map
# tm_shape(patches_sizes_km2) +  # Add borders to patches
#   tm_fill(col = "area_km2", palette = "YlOrRd", title = "area km²", interactive = TRUE) +
#   tm_borders(col = "black", lwd = 1, alpha = 0.5) + 
#   tm_layout(legend.position = c("left", "bottom"), legend.outside = T) # Adjust legend position
#   


#  Croatia ----------------------------------------------------------------

# load the required packages
library(sf)
library(dplyr)

setwd("C:/Emmanuel_Oceguera_LocalW10sys/Evirionment_R")

# Effective mesh size  
# meff = (Atotal^2) / Σ(Ai^2)

# Path to the shp
forest_patches_path <-  "I:/biocon/Emmanuel_Oceguera/projects/2023_09_Fragmentation/outputs/croatia/frag_patches_croatia.shp"
croatia_path <- "I:/biocon/Emmanuel_Oceguera/projects/2023_09_Fragmentation/data/NUTS2021_v22_Croatia.shp"

# Open files
forest_patches <- st_read(forest_patches_path)
croatia <- st_read(croatia_path)


# Effective mesh size equation 
# meff = (Atotal^2) / Σ(Ai^2)

# Define the sizes of the patches km²
patches_sizes_km2 <- forest_patches %>% 
  mutate(area_km2 = as.numeric(st_area(forest_patches)/1e6))


# Define the total area of the country
crty_total_km2 <- as.numeric(st_area(croatia)/1e6)

# Calculate the squared area of the patches and sum of squered 
patches_squared_km2 <- patches_sizes_km2$area_km2**2
sum_patches_squared_km2 <- sum(patches_squared_km2)

# Squared the total area of the country
crty_total_squared_km2 <- crty_total_km2**2

# calculate the meff using the formula
croatia_meff_km2 <- crty_total_squared_km2/sum_patches_squared_km2

# Merge meff values with the forest_patches data
forest_patches_meff <- cbind(patches_sizes_km2, meff = croatia_meff_km2)

# Print the result
cat("Effective Mesh Size (meff):", croatia_meff_km2, "Km²")

# Result 
"Effective Mesh Size (meff): 852.0644 Km²"


# Visualization of the mesh size in Estonia
# Create a ggplot object for the map
p <- ggplot() +
  geom_sf(data = croatia, fill = "lightgray") +
  geom_sf(data = forest_patches_meff, aes(fill = meff), color = NA) +
  coord_sf(crs= 3035) +
  scale_fill_gradient(low = "lightgreen", high = "darkgreen", name = "meff (km²)") +
  theme_bw(base_line_size = NA) +
  labs(title = "Effective Mesh Size (meff) Map for old grow Forest Patches in Croatia")



# Save the result as shp
output_path <- "I:/biocon/Emmanuel_Oceguera/projects/2023_09_Fragmentation/outputs/croatia"
file_name <- paste0(output_path,"/", "croatia_meffkm2.shp")
st_write(forest_patches_meff, file_name, driver = "ESRI Shapefile", overwrite= TRUE)



# # Create a choropleth map
# tm_shape(patches_sizes_km2) +  # Add borders to patches
#   tm_fill(col = "area_km2", palette = "YlOrRd", title = "area km²", interactive = TRUE) +
#   tm_borders(col = "black", lwd = 1, alpha = 0.5) + 
#   tm_layout(legend.position = c("left", "bottom"), legend.outside = T) # Adjust legend position
#   


