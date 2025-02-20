# This script is to extract habitat types from filenames of .tif files in a directory
# The habitat types are extracted based on the filename pattern 'Output_2018_Rxx_map.tif'
# where 'xx' is a number followed by an optional letter (e.g., R1, R2A, R3B, etc.)
# If the filename does not follow the pattern, the habitat type is extracted based on the pattern 'Rxx' (e.g., R1A, R2B, etc.)

# this script base on the folowwing source
https://stackoverflow.com/questions/35754058/extracting-part-of-string-by-position-in-r

# Define the directory path
dir_path <- "I:/biocon/Nikolaj_Poulsen/Fragmentation_project/EUNIS Habitats/Fragmentations maps/2018/R"

# Check if the directory exists
if (dir.exists(dir_path)) {
  # List all .tif files in the directory
  tif_files <- list.files(path = dir_path, pattern = "\\.tif$", full.names = TRUE)
  
  # Extract habitat types from filenames
  habitat_types <- sapply(tif_files, function(file) {
    file_name <- basename(file)
    
    # Check if the filename follows the 'Output_2018_Rxx_map.tif' format
    habitat_type <- gsub("Output_2018_(R[0-9]+[A-Za-z]*)_map\\.tif", "\\1", file_name)
    
    # If no match, handle cases like 'R1A', 'R2B', etc. (no 'Output_2018_' prefix)
    if (file_name == habitat_type) {
      habitat_type <- gsub("^(R[0-9]+[A-Za-z]*)$", "\\1", file_name)
    }
    return(habitat_type)
  })
  
  # Remove duplicates to create a unique list of habitat types
  unique_habitat_types <- unique(habitat_types)
  
  # Print the unique habitat types
  print(unique_habitat_types)
} else {
  cat("Directory not found!")
}
length(unique_habitat_types)
