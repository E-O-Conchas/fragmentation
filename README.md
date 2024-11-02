# Fragmentation Analysis Workflow
## Need to be updated
## Introduction
This document outlines the comprehensive workflow for a moving window fragmentation analysis, incorporating methodologies to process spatial data effectively.


## Steps
1. **Create the basemaps for the input in GRASS GIS using R: This code need to be provided by Nikolaj**

2. **Clump analysis, create tiles and export them**
   - Load Raster to GRASS GIS
   	- [Import tiles to GRASS GIS](fragmentation/01.load_vrt_to_grass.py)

   - Compute the clump analysis, create 1000m X 1000m tiles and export them in the defined folder  


1. **Tile Raster Inside GRASS GIS, run Clumps analysis and Export**
   - Load Raster or VRR to GRASS GIS
	 

   - Run Clump Function on Full Raster
	 - [Clumps Full Raster and Report in GRASS Script](https://github.com/E-O-Conchas/fragmentation/blob/main/6.clumps_full_raster_and_report_GRASS.py)
   
   - Tile Raster and Export Files in GRASS GIS
   - Before Export Tiles, create a Mask to export only forest polygons
	 - [Create Tiles and Export Files in GRASS Script](https://github.com/E-O-Conchas/fragmentation/blob/main/7.create_tiles_and_export_files_GRASS.py)

3. **Delete Empty Tiles**
   - [Delete Empty Tiles Script](https://github.com/E-O-Conchas/fragmentation/blob/main/8.delete_empty_tiles.py)

4. **Aggregate Rasters to 1km Resolution**
   - [Aggregate Tiles 5m to 1k Script](https://github.com/E-O-Conchas/fragmentation/blob/main/9.tiles_to_1km_optimized.py)

5. **Calculate Fragmentation Per Pixel with a Moving Window**
   - [Calculate Fragmentation Index Script](https://github.com/E-O-Conchas/fragmentation/blob/main/10.fragmentation_indicatior_cal.py)

6. **Create VRT from the results **
   - [Generate VRT file with the fragmentation results](https://github.com/E-O-Conchas/fragmentation/blob/main/11.convert_result_to_vrt.py)

## Source Data
- need to be fill it

## Output Data
- Raster files indicating the fragmentation index and other metrics.

## Additional Notes
- Ensure all software and libraries are correctly configured and installed.
- Verify data integrity at each step.

## Conclusion
This workflow provides a structured and detailed approach for analyzing forest fragmentation, utilizing a suite of scripts for comprehensive analysis.

## Author
- need to be fill it
