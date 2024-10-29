# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 12:39:02 2023

@author: no67wuwu

Description: This script performs fragmentation analysis.
             It calculates fragmentation indices based on the percentage of area 
             covered by each fragment and outputs the results as raster files.
 
Note: Before running this script check the function get_tiles.

"""

import os
import numpy as np
import pandas as pd
from glob import glob
import rasterio
from multiprocessing import Pool
import time

# Fragmentation function to calculate the fragmentation index as a percentage
def frag_ind(s):
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
                nodata=nodata,
                transform=src.transform,
                crs=src.crs
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
def get_tiles(tile):
    """
    Get surrounding tiles for a given tile.
    
    Parameters:
    tile (str): Path to the central tile.
    
    Returns:
    numpy array: Combined array of the central tile and its surroundings.
    
    Note: Before running the script you might need to change the initial name of the tiles.
    """
    name = tile.split(os.sep)[-1]
    y_top = int(name.split('-')[1]) - 1
    y_bot = y_top + 2
    x_left = int(name.split('-')[2].split('.')[0]) - 1
    x_right = x_left + 2
    
    # Generate list of surrounding tiles
    # Change the tiles names and uncomment this before running 
    # sur_tiles = ['Tile_name-{}-{}.tif'.format(('000' + str(y))[-3:], ('000' + str(x))[-3:]) 
                  # for y in range(y_top, y_bot + 1)  
                  # for x in range(x_left, x_right + 1)]
     
    # Map each tile to its position in the combined array↕
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
    
    
    print(f"bbox for center ({x},{y}): xmin={xmin}, xmax={xmax}, ymin={ymin}, ymax={ymax}")
    return xmin, xmax, ymin, ymax

# Function to create directories if they don't exist
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)



# Main function to process each tile
def main(tile):
    """
    Process a tile to calculate fragmentation indices and write output rasters.
    
    Parameters:
    tile (str): Path to the tile to be processed.
    
    Returns:
    str: Confirmation message.
    """
    raster = get_tiles(tile)
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
                
                frag_indi_counts = frag_ind(window_counts)
                
                df_window = df_rep_subset.loc[df_rep_subset['frag_id'].isin(window_ids)]
                df_window_array = np.array(df_window['area'] / (1000 * 1000)).astype(int)
                frag_indi_orig = frag_ind(df_window_array)
                
                
                # Inside your loop where you calculate the output values:
                # out_count_area[x - 1000, y - 1000] = np.clip(int(frag_indi_counts), 0, 100)
                # out_orig_area[x - 1000, y - 1000] = np.clip(int(frag_indi_orig), 0, 100)

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

# Define paths to input files and output directory
# tile_path = r"S:\username\fragmentation_maps\baseline\test"
# report_path = r"S:\username\fragmentation_maps\baseline\report_unique_areas_and_units.ini"

tile_path = r"S:\username\fragmentation_maps\EUNIS\bfragmap2_tiles_clumps_EUNIS"
report_path = r"S:\username\fragmentation_maps\EUNIS\bfragmap2_tiles_clumps_EUNIS\report_unique_areas_and_units.ini"

# Read the report file and process the data
df_report = pd.read_csv(report_path, sep='|', skiprows=15, skipfooter=3, names=['a', 'frag_id', 'b', 'area', 'c'], thousands=',', engine='python')
df_report = df_report.loc[:, ['frag_id', 'area']]

#outpath = r"S:\Emmanuel_OcegueraConchas\fragmentation_maps\baseline\bfrahmap_test"
outpath = r"S:\username\fragmentation_analysis\EUNIS\base_fragmentation_map2_EUNIS\bfragmap2_meff_EUNIS"
log = open(outpath + '\\frag_ind_per.log', 'w')

# Get list of tiles to process
tiles = glob(tile_path + r'\*.tif')
sur_radius = 50# Radius of cells for surrounding the center_pixel

# Execute the script using multiprocessing
if __name__ == '__main__':
    start_time = time.time()
    pool = Pool(10)
    for bar in pool.imap_unordered(main, tiles):
        log.write(bar)
        log.flush()

    log.close()
    end_time = time.time() # End time
    elapsed_time = end_time - start_time
    print(f'Total time taken: {elapsed_time:.2f} seconds')

