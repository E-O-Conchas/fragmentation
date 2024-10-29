### This script is used to rasterize the road data. The road data is stored in a shapefile format. 
### The script  raster file.

# We clean the envrioment
rm(list=ls())
gc()

getwd()

# load the libraries we 
library(terra)

# rooth path: This is the path to the folder where the road data is stored
root_path <- "S:\\Nikolaj_Poulsen\\Fragmentation\\Roads"

# We list the files in the folder
list.path <- list.files(path = root_path, pattern = ".shp$", full.names = TRUE)

# open the shapefile
road_data <- vect(list.path) 
# plot(road_data) # Not neccesary because takes a lot of time

# We will use the extent and resolution from the raster file that we have already created
# we take the baseline raster as a base map 
base_raster <- rast("I:\\biocon\\Nikolaj_Poulsen\\Fragmentation_project\\Cropped\\Baseline2000.tif")

# We reproject the road data because it does not have the same CRS
road_data_3035 <- project(road_data, crs(base_raster))

# We create an empty raster with the same extent and resolution as the base raster
ext <- ext(base_raster)
res <- res(base_raster)

raster_template <- rast(ext = ext, 
                        res = res, 
                        crs = crs(base_raster))

# Rasterize the road data
raster <- rasterize(road_data_3035, raster_template, background=NA ,field = 1)

# Plot the rasterized output
plot(raster)

# save the raster in the folder
output_path <- paste0(root_path, '/eu_roads.tiff')

# Write the file
writeRaster(raster, 
            output_path, 
            overwrite=TRUE,
            gdal=c("COMPRESS=NONE", "TFW=YES"))

# We convert this to a binary map
binary_raster <-  classify(raster, cbind(0, Inf, 1))

binary_raster[is.na(binary_raster)] <- 0

plot(binary_raster)

# we crop it using a eu eu shape mask
eu_mask <- vect("I:\\biocon\\Nikolaj_Poulsen\\Fragmentation_project\\Europe\\eu_mask_single.shp")
plot(eu_mask)

binary_raster_crop <- terra::crop(binary_raster, eu_mask, mask = T)

plot(binary_raster_crop)


# save the raster in the folder
output_path <- paste0(root_path, '/eu_roads_binary_cropped.tiff')

# Write the output
writeRaster(binary_raster_crop, 
            output_path, 
            overwrite=TRUE,
            gdal=c("COMPRESS=NONE", "TFW=YES"))


#### rasterize resolution 100m

# Define the output names 
road_output_100m <- paste0(root_path, '/eu_roads_100m.tif')
road_output_binary_cropped_100m <- paste0(root_path, '/eu_roads_binary_cropped_100m.tif')


# We create an empty raster with the same extent and resolution 100m
ext <- ext(base_raster)
res <- c(100, 100) # 100 meter

raster_template_100m <- rast(ext = ext,
                             res = res,
                             crs = crs(base_raster))

# Rasterize the road data
raster <- rasterize(road_data_3035, raster_template_100m, background=NA ,field = 1)
plot(raster)

# Write the output
writeRaster(raster, 
            road_output_100m, 
            overwrite=TRUE,
            gdal=c("COMPRESS=NONE", "TFW=YES"))

# We convert this to a binary map
binary_raster_100m <-  classify(raster, cbind(0, Inf, 1))

binary_raster_100m[is.na(binary_raster_100m)] <- 0
plot(binary_raster_100m)

# we crop it using a eu eu shape mask
binary_raster_100m_crop <- terra::crop(binary_raster_100m, eu_mask, mask = T)
plot(binary_raster_100m_crop)


# Write the output
writeRaster(binary_raster_100m_crop, 
            road_output_binary_cropped_100m, 
            overwrite=TRUE,
            gdal=c("COMPRESS=NONE", "TFW=YES"))



# save 
save.image("18102024.RData")


