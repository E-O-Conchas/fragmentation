# Fragmentation Analysis Workflow

This document provides a step-by-step workflow for performing a moving window fragmentation analysis, using methods to efficiently process large spatial datasets.

## Steps
1. **Generate Basemaps in GRASS GIS using R**
   - The initial step involves creating basemaps in GRASS GIS as input for fragmentation analysis. 
   - **Note:** Code for this step will be provided by Nikolaj.

3. **Clump Analysis, Tiling, and Export**

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



## Output Data
- Raster files indicating the fragmentation index and other metrics.

## Additional Notes
- Ensure all software and libraries are correctly configured and installed.
- Verify data integrity at each step.

## Conclusion
This workflow provides a structured and detailed approach for analyzing forest fragmentation, utilizing a suite of scripts for comprehensive analysis.

