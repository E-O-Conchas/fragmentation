# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 12:39:02 2023

@author: no67wuwu

Description: This script performs fragmentation analysis.
             It calculates fragmentation indices based on the percentage of area 
             covered by each fragment and outputs the results as raster files.
"""
import time
import os
import numpy as np
import pandas as pd
from glob import glob
import rasterio
from multiprocessing import Pool
from osgeo import gdal

# Fragmentation function to calculate the fragmentation index as a percentage
def frag_ind(s, sur_radius):
    """
    Calculate the fragmentation index as a percentage.
    
    Parameters:
    s (iterable): List of cell counts or areas.
    
    Returns:
    float: Fragmentation index as a percentage.
    """
    area = ((sur_radius * 2) + 1) ** 2
    a = map(lambda x: x / area, s)
    a = sum(a) * 100
    return a

# Function to read a TIFF file and return a numpy array
def read_tif(tif, band=1, nodata=False):
    """
    Reads in a TIFF file and returns a numpy array.
    
    Parameters:
    tif (str): Full path to the TIFF file.
    band (int or list): The band number(s) to read. Default is 1.
    nodata (bool): Whether to return the no data value. Default is False.
    
    Returns:
    numpy array or tuple: The read data (and nodata value if specified).
    """
    def read_data(dataset, band_nr):
        band_data = dataset.read(band_nr)
        if nodata:
            nodata_value = dataset.nodata
            return band_data, nodata_value
        return band_data

    with rasterio.open(tif) as dataset:
        if band == 0:
            band_list = list(range(1, dataset.count + 1))
        elif isinstance(band, int):
            band_list = [band]
        elif isinstance(band, list):
            if max(band) > dataset.count:
                raise ValueError('Max value in the band list exceeds the number of bands in the raster.')
            band_list = band
        else:
            raise ValueError('Invalid band parameter.')

        if len(band_list) == 1:
            return read_data(dataset, band_list[0])
        else:
            stack = np.stack([read_data(dataset, b) for b in band_list])
            return stack

# Function to write a numpy array to a TIFF file
def write_tif(file_with_srid, full_output_name, data, dtype=1, nodata=None, option=False):
    """
    Write data to a TIFF file.
    
    Parameters:
    file_with_srid (str): Path to the original file with spatial information.
    full_output_name (str): Path to the output TIFF file.
    data (numpy array): Data to write.
    dtype (int): Output data type. Default is 1 (Int32).
    nodata (int or float, optional): No data value. Default is None.
    option (str, optional): Compression option. Default is False.
    """
    dtypeL = [
        rasterio.int16,
        rasterio.int32,
        rasterio.uint16,
        rasterio.uint32,
        rasterio.float32,
        rasterio.float64,
        rasterio.uint8
    ]
    
    try:
        with rasterio.open(file_with_srid) as src:
            profile = src.profile
            profile.update(
                dtype=dtypeL[dtype],
                count=data.shape[0] if data.ndim == 3 else 1,
                compress='deflate' if option else None,
                nodata=nodata
            )

            with rasterio.open(full_output_name, 'w', **profile) as dst:
                if data.ndim == 2:
                    dst.write(data, 1)
                else:
                    for i in range(data.shape[0]):
                        dst.write(data[i], i + 1)
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
    except ValueError:
        print("Could not write the nodata value")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Function to get surrounding tiles for a given tile
def get_tiles(tile, tiles, habitat, year):   
    """
    Get surrounding tiles for a given tile.

    Parameters:
    tile (str): Path to the central tile.
    tiles (list): List of all tile paths.
    habitat (str): Habitat type (e.g., "N21", "R31").
    year: (int): Year of the dataset (e.g. 2018, 2020...)

    Returns:
    numpy array: Combined array of the central tile and its surroundings.
    
    """
    # check if the Tiles list is empty
    if not tiles:
        raise ValueError('No tiles found')
    
    name = os.path.basename(tile)
    # print(f"this is the full tiff name: {name}")
    # folder_name = os.path.basename(os.path.dirname(tile))
    
    # Construct the base name dinamically using habitat
    # base_name = f"{habitat}_{year}_{folder_name.split('_')[0]}_clump"
    base_name = f"{habitat}_{year}_clump_tile"

    # print(f"This is the base name: { base_name}" )
    # example of a base name:
    # R42_2018_bfragmap2_clump-000-002.tif
    
    # # Extract the base name pattern based on the folder
    # if "bfragmap_tiles_clumps_EUNIS" in folder_name:
    #     base_name = "T1B_2000_bfragmap_clump"
    #     #print(base_name)
    # elif "bfragmap1_tiles_clumps_EUNIS" in folder_name:
    #     base_name = "T1B_2000_bfragmap1_clump"
    #     #print(base_name)
    # elif "bfragmap2_tiles_clumps_EUNIS" in folder_name:
    #     base_name = "T1B_2000_bfragmap2_clump"
    #     #print(base_name)
    # else:
    #     raise ValueError("Unknown folder name pattern.")
    
    
    y_top = int(name.split('-')[1]) - 1
    y_bot = y_top + 2
    x_left = int(name.split('-')[2].split('.')[0]) - 1
    x_right = x_left + 2
    
    # Generate list of surrounding tiles with consistent 3-digit padding
    sur_tiles = [f"{base_name}-{y:03d}-{x:03d}.tif"
                  for y in range(y_top, y_bot + 1)  
                  for x in range(x_left, x_right + 1)]
     
    # Map each tile to its position in the combined array
    pos_dic_tiles = {}
    pos = ['0,0','0,1','0,2',
           '1,0','1,1','1,2',
           '2,0','2,1','2,2']
    pos_count = 0
    for st in sur_tiles:
        pos_dic_tiles[st] = pos[pos_count]
        pos_count += 1
    
    # Get paths to existing tiles
    sur_tile_paths = [x for x in tiles for y in sur_tiles if y in x]
    
    # Create an empty array and fill with data from surrounding tiles
    array = np.zeros([3000, 3000])
    array.fill(-1)
    for stp in sur_tile_paths:
        stp_name = stp.split(os.sep)[-1]
        sub_rast = read_tif(stp)
        
        if sub_rast.shape != (1000, 1000):
            print(f"Unexpected shape for {stp_name}: {sub_rast.shape}")
            continue

        ymin = int(pos_dic_tiles[stp_name].split(',')[0]) * 1000
        ymax = ymin + 1000
        xmin = int(pos_dic_tiles[stp_name].split(',')[1]) * 1000
        xmax = xmin + 1000
        array[ymin:ymax, xmin:xmax] = sub_rast
    
    return array

# Function to get bounding box coordinates for a given center pixel
def bbox(x, y, sur_radius):
    """
    Get bounding box coordinates.
    
    Parameters:
    x (int): X-coordinate of the center pixel.
    y (int): Y-coordinate of the center pixel.
    sur_radius (int): Radius for surrounding cells.
    
    Returns:
    tuple: Bounding box coordinates (xmin, xmax, ymin, ymax).
    """
    xmin = x - sur_radius
    xmax = x + sur_radius + 1
    ymin = y - sur_radius
    ymax = y + sur_radius + 1
    return xmin, xmax, ymin, ymax

# Function to create directories if they don't exist
def ensure_dir(directory):
    """
    Ensure that the directory exists.

    Parameters:
    directory (str): Path to the directory.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

# Main function to process each tile
def main(args):
    tile, tiles, df_report, outpath, sur_radius, habitat, year = args
    """
    Process a tile to calculate fragmentation indices and write output rasters.
    
    Parameters:
    tile (str): Path to the tile to be processed.
    
    Returns:
    str: Confirmation message.
    """
    raster = get_tiles(tile, tiles, habitat, year)
    #print(f"Unique values in raster for tile {tile}: {np.unique(raster)}")
    orig_raster = read_tif(tile)
    out_count_area = np.zeros(orig_raster.shape)
    out_orig_area = np.zeros(orig_raster.shape)
    
    frag_ids = np.unique(raster[:,:]) 
    frag_ids = np.delete(frag_ids, np.where(frag_ids == 0))
    df_rep_subset = df_report.loc[df_report['frag_id'].isin(frag_ids)]
    
    for x in range(1000, 2000):
        for y in range(1000, 2000):
            if raster[x, y] != 0:
                xmin, xmax, ymin, ymax = bbox(x, y, sur_radius)
                s_cells = raster[xmin:xmax, ymin:ymax]
                window_ids, window_counts = np.unique(s_cells, return_counts=True)
                if 0 in window_ids:
                    window_ids = window_ids[1:]
                    window_counts = window_counts[1:]
                
                frag_indi_counts = frag_ind(window_counts, sur_radius)
                
                df_window = df_rep_subset.loc[df_rep_subset['frag_id'].isin(window_ids)]
                df_window_array = np.array(df_window['area'] / (1000 * 1000)).astype(int)
                frag_indi_orig = frag_ind(df_window_array, sur_radius)
                
                out_count_area[x - 1000, y - 1000] = int(frag_indi_counts + 0.5)
                out_orig_area[x - 1000, y - 1000] = int(frag_indi_orig + 0.5)
    
    # Ensure output directories exist
    window_count_dir = os.path.join(outpath, "window_count3")
    # originarea_count_dir = os.path.join(outpath, "originarea_count3")
    
    ensure_dir(window_count_dir)
    #ensure_dir(originarea_count_dir)
    
    # Write output raster considering pixel counts
    outraster_counts = os.path.join(window_count_dir, os.path.basename(tile))
    write_tif(tile, outraster_counts, out_count_area, 1)
    
    # Write output raster considering original areas
    #outraster_orig_area = os.path.join(originarea_count_dir, os.path.basename(tile))
    #write_tif(tile, outraster_orig_area, out_orig_area, 1)
    
    return 'tile: {} written'.format(tile.split(os.sep)[-1])

# Function to check if the folder is ready
def is_folder_ready_for_processing(folder_path):
    """
    Check if the folder has a 'READY.txt' flag file indicating that it is ready for processing.
    
    Parameters:
    folder_path (str): Path to the folder to check.
    
    Returns:
    bool: True if the folder is ready for processing, False otherwise.
    """
    return os.path.exists(os.path.join(folder_path, 'READY.txt'))

# funtion to create a mosaic of all tiles
def mosaic_tiles(output_path, habitat_code, year, subfolder="window_count3"):
    """
    Create a mosaicked GeoTIFF from all tile TIFFs in the given subfolder.
    
    Parameters:
    output_path (str): The path to the habitat output folder.
    habitat_code (str): The habitat code (e.g., Q21).
    year (int): Year of the dataset.
    subfolder (str): Subfolder where the tiles are stored (default: window_count3).
    """
    tile_dir = os.path.join(output_path, subfolder)
    if not os.path.exists(tile_dir):
        print(f"[Mosaic] No folder found for habitat: {habitat_code}")
        return

    tiff_tiles = [os.path.join(tile_dir, f) for f in os.listdir(tile_dir) if f.endswith(".tif")]
    if not tiff_tiles:
        print(f"[Mosaic] No TIFF tiles found for: {habitat_code}")
        return
    
    print(f"[Mosaic] Creating mosaic for {habitat_code} with {len(tiff_tiles)} tiles...")
    
    vrt = gdal.BuildVRT('', tiff_tiles)
    mosaic_output = os.path.join(output_path, f"{habitat_code}_{year}_mosaic.tiff")
    
    gdal.Translate(
        mosaic_output,
        vrt,
        format='GTiff',
        outputType=gdal.GDT_UInt16,
        creationOptions=['COMPRESS=DEFLATE']
    )
    
    print(f"[Mosaic] Mosaic created for {habitat_code} at {mosaic_output} !!")


if __name__ == '__main__':

    # Start the time counter
    start_time = time.time()
    
    year = 2012
    habitats_groups = ['N', 'Q', 'R', 'S', 'T', 'U', 'V']
    sur_radius = 50
    base_input_root = r"S:\Emmanuel_OcegueraConchas\fragmentation_maps_tiles_and_input\Input_layers\EUNIS_tiles"
    base_output_root = r"D:\Emmanuel_Oceguera\Fragmentation_analysis\output\EUNIS" 

    # Loop over the groups of habitats
    # take only the first element of the list for this time 15.05.2025
    for group in habitats_groups[2:]: # This time we are going to process only the first group
        print(f"Processing group: {group}")
        group_folder = os.path.join(base_input_root, str(year), group)
        habitats = os.listdir(group_folder)

        for habitat_code in habitats:
            # if habitat_code != 'Q63': # Skip the rest of the habitats
            #     continue
            print (f"Processing habitat: {habitat_code}")
            tile_input_path = os.path.join(group_folder, habitat_code)
            if not is_folder_ready_for_processing(tile_input_path):
                print(f"Waiting for {habitat_code} to be ready...")
                while not is_folder_ready_for_processing(tile_input_path):
                    time.sleep(150) # 2.5 min
                    
            print(f"folder {habitat_code} is ready. Starting the process...")
            output_path = os.path.join(base_output_root, str(year), group, habitat_code)
            ensure_dir(output_path)
       
            report_path = os.path.join(tile_input_path, "report_unique_areas_and_units.ini")
            log_file_path = os.path.join(output_path, 'frag_ind_pct.log')          
            
            # Read the report file and process the data
            df_report = pd.read_csv(
                report_path, sep='|', skiprows=15, skipfooter=3,
                names=['a', 'frag_id', 'b', 'area', 'c'], 
                thousands=',', engine='python'
            )
            
            df_report = df_report.loc[:, ['frag_id', 'area']]
            print("The report data frame has benn created")
            
            # Set the log file path for this folder
            # Get list of tiles to process
            # tiles = glob(tile_input_path + '//*.tif')
            tiles = glob(os.path.join(tile_input_path, "*.tif"))           
            
            with open(log_file_path, 'w') as log, Pool(60) as pool:
                args = [(tile, tiles, df_report, output_path, sur_radius, habitat_code, year) for tile in tiles]
                for bar in pool.imap_unordered(main, args):
                    log.write(bar + '\n')
                    log.flush()
            log.close()
            print(f"Fragmentation analysis for {habitat_code} has been completed")

            # Add the mosaic function to create a mosaic of all tiles
            mosaic_tiles(output_path, habitat_code, year)
            print(f"Mosaic for {habitat_code} has been created")
    # End the time counter
    end_time = time.time() # End time
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time/3600:.2f} hours")


    # calculated time in hours: 17.773467040194405
    # The process took 17 hours to finish all the R habitats for the year 2018
    # It should be noticed that the time calculates the waiting time for the folders to be ready
    # So this time is for the full proccess of the fragmentation analysis, incluiding the clumping and
    # the tilin and exporting the tiles from GRASS GIS



