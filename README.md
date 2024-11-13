# Fragmentation Analysis Workflow  <img align="right" width="15%" src="images/logo.jpeg"> 
 
This document provides a step-by-step workflow for performing a moving window fragmentation analysis, using methods to efficiently process large spatial datasets.

## Steps
1. **Generate input maps for GRASS GIS using R**
   - The initial step involves creating basemaps with different fragmentation barriers as input for analysis. 
   - **Note:** Code for this step will be provided by Nikolaj.

2. **Clump Analysis, Tiling, and Export**

   in this step, contiguous regions or "clumps" within the raster data are identified, tiled into manageable sections, and exported. These processes are essential for handling large spatial datasets and preparing them for fragmnetation analysis.
   
   - **Load Raster Data into GRASS GIS**

      Raster data is imported into GRASS GIS to make it accessible for processing and analysis.
     	- Refer to [Import tiles to GRASS GIS](https://github.com/E-O-Conchas/fragmentation/blob/7c56ac37c6174fcb428483b30376997a3fc678d7/01.load_vrt_to_grass.py) for the loading process.

   - **Perform Clump Analysis and Generate Clump Reports**
  
     Clump analysis groups contiguous regions with similar values, assigning unique IDs to each "patch" within the landscape. This process is essential for fragmentation metrics, as it helps identify distinct areas within the raster. A report is generated detailing key metrics for each clump, such as area and distribution, which aids in understanding spatial fragmentation patterns.

   - **Create 1000m x 1000m Tiles**
  
     To enable parallel processing and facilitate handling of large datasets, the clump maps are divided into 1000m x 1000m tiles. This approach allows efficient processing by working with individual tiles.
   
   - **Export Tiles to GeoTIFF Format**  

     Each tile is exported in GeoTIFF format, ensuring compatibility with various GIS platforms and enabling easy sharing and further analysis outside of GRASS GIS. Once all steps are complete, a `READY.txt` file is generated in the output folder to indicate that preprocessing is finished.
   
       - Refer to [Clump Analysis, Tiling, and Export](https://github.com/E-O-Conchas/fragmentation/blob/7c56ac37c6174fcb428483b30376997a3fc678d7/02.clumps_analysis_tiles_and_export.py) for the full script.

3. **Compute Effective Mesh Size Fragmentation Metric Using Moving Window Approach**

   In this step, we calculate the effective mesh size (meff) using a moving window approach to quantify fragmentation within the landscape. The effective mesh size is a metric that assesses how well-connected or fragmented the landscape is, based on the size and distribution of contiguous "patches" within each window. This analysis runs over each 1000m x 1000m tile created in the previous step and outputs a raster file representing the fragmentation metric (%) for each tile.
   
   - **Load Clump Tiles for Analysis**  
     Each tile generated from the clump analysis is processed individually, accessing surrounding tiles to maintain continuity across edges within the moving window analysis.

   - **Define Moving Window Radius**  
     A specific `sur_radius` is used to define the moving window size, impacting connectivity and fragmentation analysis by determining the extent of neighboring cells included in each calculation.

   - **Calculate Fragmentation Index**  
     For each central cell in the tile, the fragmentation index is calculated as a percentage, reflecting the degree of fragmentation within the defined moving window radius based on the number of unique patches (or clumps) within that area. The function `frag_ind` computes the fragmentation index by dividing the area covered by each clump by the total area of the window, normalizing the index to capture the density and distribution of clumps.

   - **Output Fragmentation Metrics as Raster Files**  
     The calculated fragmentation metrics for each tile are saved as raster files in GeoTIFF format, compatible with various GIS platforms, allowing easy sharing and further analysis. Separate folders for each map type (Baseline, Fragmentation1, Fragmentation2) organize the outputs.

     - Refer to [Fragmentation Analysis Script](https://github.com/E-O-Conchas/fragmentation/blob/f55dc3c1dca43410e8a705073abcbabd9bc67f62/03.fragmentation_indicator_multiple_folders.py) for the full code.

4. **Merge Processed Tiles for Final Output**  
   Once all tiles are processed, they are merged into a single GeoTIFF file representing the entire study area, providing a comprehensive view of the fragmentation metrics across the landscape.

     




