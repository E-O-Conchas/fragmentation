# Clean the environment
rm(list = ls())
gc()


# how you would install ebvcube if from CRAN
install.packages('ebvcube') # (not recomended)

#install latest dev version from GitHub
devtools::install_github('https://github.com/LuiseQuoss/ebvcube/tree/dev')

#in case you get an error for libaries: rhdf5, HDF5Array or DelayedArray
#(those are packages from BioConductor)
# install.packages('BiocManager')
# BiocManager::install("rhdf5")
# BiocManager::install("HDF5Array")
# BiocManager::install("DelayedArray")


# Import libraries
library(ebvcube)
library(terra)

# define the ouput folder
outputdir <- "S:/Emmanuel_OcegueraConchas/meff_all_years_result/EUNIS_data/"

# Define the EBV ID we want to doenload
datasets <- ebv_download()

# Download the file
# we use the id number in this case is the number 3 by Stephan Hennekens
# spatial resolution of 1km X 1km
ebv_file <- ebv_download(id = datasets$id[3], outputdir)
print(ebv_file)

# Set the path to the file
file <- "S:/ebv_portal/15/fernandez_ecostr_id15_20220731_v2.nc"
# file <-  file.path(outputdir, "hennekens_ecostr_id3_20220208_v2.nc")

# We check the properties files
prop.file <- ebv_properties(file, verbose = FALSE)
prop.file@general[1:4]
prop.file@spatial

slotNames(prop.file)

# We get the path to all existing data cubes
datacubes <- ebv_datacubepaths(file, verbose=FALSE)
# Result
# > datacubes
# datacubepaths                       metric_names
# 1 metric_1/ebv_cube Probability of habitat suitability

# We also check the properties od the specifc data cube
prop.dc <- ebv_properties(file, datacubes[2,1], verbose = FALSE)
prop.dc@metric # check the name of metric
prop.dc@temporal$dates # Check the temporal we have two timesteps 
# [1] "2014-01-01" "2019-01-01"

# Data cube path
dc <- datacubes[2, 1]

# Extract the data for Acidophilous Quercus forest for the two time steps
ebv_data_all_times <- ebv_read(filepath = file,
                               datacubepath = dc,
                               entity = "Acidophilous Quercus forest",
                               timestep = 1)
plot(ebv_data_all_times)

# # Extract the data for Acidophilous Quercus forest for timestep 1 <- "2014-01-01" 
# ebv_data_time1 <- ebv_read(filepath = file,
#                            metric = 1,
#                            entity = "Acidophilous Quercus forest",
#                            timestep = 1)
# plot(ebv_data_time1)
# 
# # Extract the data for Acidophilous Quercus forest for timestep 2 <- "2019-01-01" 
# ebv_data_time2 <- ebv_read(filepath = file,
#                      metric = 1,
#                      entity = "Acidophilous Quercus forest",
#                      timestep = 2)
# plot(ebv_data_time2)

# We save the subtract in the output folder

# Export as GeoTIFF for compatibility with GIS software
terra::writeRaster(ebv_data_all_times, 
                   file.path(outputdir, "ebvdata_AciQue_forest_2010_m2_100m.tif"),
                   overwrite = TRUE)












