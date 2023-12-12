# Forest Fragmentation Analysis Workflow

## Introduction
This document outlines the comprehensive workflow for forest fragmentation analysis, incorporating various scripts and methodologies to process spatial data effectively.

## Rationale
The analysis is crucial to understand the impact of environmental changes on forest ecosystems, providing insights into the areas of fragmentation and potential conservation strategies.

## Goal
To assess forest fragmentation by transforming spatial data into actionable insights through advanced geospatial analysis.

## Workflow Steps
	1. **Convert Shapefile to Raster Tiles (Resolution 5m per Pixel)**
	   - Load shapefile to PostgreSQL.
	   - Create raster tiles, mask, and fragmentation:
		 - [Rasterize Fragmentation 5m Script](https://github.com/E-O-Conchas/fragmentation/blob/main/1.rasterize_mask_and_fragmentation_5m.py)
	   
	   - Combine mask and fragmentation:
		 - [Combine Frag Mask Tiles Script](https://github.com/E-O-Conchas/fragmentation/blob/main/2.combine_mask_and_fragmentation_tiles_gdal.py)
	   
	   - Generate list of valid tiles:
		 - [Get Valid Tiles Script](https://github.com/E-O-Conchas/fragmentation/blob/main/3.generate_list_valid_tiles.py)
	   
	   - Create VRT from valid tiles:
		 - [Create VRT Script](https://github.com/E-O-Conchas/fragmentation/blob/main/4.create_vrt_from_valid_tiles.py)
	   

	2. **Tile Raster Inside GRASS GIS, run Clumps analysis and Export**
	   - Load VRT to GRASS GIS
		 - [Import tiles to GRASS GIS](https://github.com/E-O-Conchas/fragmentation/blob/main/5.load_vrt_to_grass.py)

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