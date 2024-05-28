# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 12:39:02 2023

@author: no67wuwu

Description: This script performs fragmentation analysis on urban ot other land use raster tiles.
             It calculates fragmentation indices based on the percentage of area 
             covered by each fragment and outputs the results as raster files.
"""

import os
import numpy as np
import pandas as pd
from glob import glob
import rasterio
from multiprocessing import Pool

# Fragmentation function to calculate the effective mesh size index as a percentage
def frag_ind(s):
    """
    Calculate the fragmentation index as a percentage.
    
    Parameters:
    s (iterable): List of cell counts or areas.
    
    Returns:
    float: Fragmentation index as a percentage.
    
    """
    area = ((sur_radius*2)+1)**2
    a = map(lambda x: x**2, s)
    a = sum(a)*1.0/area
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
def get_tiles(tile):
    """ 
    Get surrounding tiles for a given tile.
    
    Parameters:
    tile (str): Path to the central tile.
    
    Returns:
    numpy array: Combined array of the central tile and its surroundings.
    """
    name = tile.split(os.sep)[-1]
    y_top = int(name.split('-')[1])-1
    y_bot = y_top + 2
    x_left = int(name.split('-')[2].split('.')[0])-1
    x_right = x_left + 2
    
    # Generate list of surrounding tiles
    sur_tiles = ['name_of_the_tile-{}-{}.tif'.format(('000'+str(y))[-3:], ('000'+str(x))[-3:]) 
            for y in range(y_top, y_bot+1)  
                for x in range(x_left, x_right+1) ]
     
    # Map each tile to its position in the combined array               
    pos_dic_tiles = {}
    pos = ['0,0','0,1','0,2',
           '1,0','1,1','1,2',
           '2,0','2,1','2,2']
    pos_count = 0
    for st in sur_tiles:
        pos_dic_tiles[st] = pos[pos_count]
        pos_count +=1
    
    # Get paths to exisitng tiles
    sur_tile_paths = [x for x in tiles for y in sur_tiles if y in x]
    
    # Create an empty array and fill with data from so=urrounding tiles
    array = np.zeros([300,300])
    array.fill(-1)
    for stp in sur_tile_paths:
        stp_name = stp.split(os.sep)[-1]
        sub_rast = read_tif(stp)
        
        # Check the shape of the sub_rast
        if sub_rast.shape != (100, 100):
            print(f"Unexpected shape for {stp_name}: {sub_rast.shape}")
            continue 

        # Fill position based on the position dic
        ymin = int(pos_dic_tiles[stp_name].split(',')[0]) * 100
        ymax = ymin +100
        xmin = int(pos_dic_tiles[stp_name].split(',')[1]) * 100
        xmax = xmin + 100
        array[ymin:ymax, xmin:xmax] = sub_rast
    
    return array

# Function to get bounding box coordinates for a given center pixel
def bbox(x,y, sur_radius):
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

# Main function to process each tile
def main(tile):
    """
    Process a tile to calculate fragmentation indices and write output rasters.
    
    Parameters:
    tile (str): Path to the tile to be processed.
    
    Returns:
    str: Confirmation message.
    """
    # Get surrownding tiles
    raster = get_tiles(tile)
    orig_raster = read_tif(tile)
    out_count_area = np.zeros(orig_raster.shape)
    out_orig_area = np.zeros(orig_raster.shape)
    
    frag_ids = np.unique(raster[:,:])  
    frag_ids = np.delete(frag_ids, np.where(frag_ids==0))
    df_rep_subset = df_report.loc[df_report['frag_id'].isin(frag_ids)]
    
    for x in range(100,200):
        for y in range(100, 200):
            if raster[x,y]!=0:
                # Get surrounding cells
                xmin, xmax, ymin, ymax = bbox(x, y, sur_radius)
                s_cells = raster[ xmin : xmax, ymin : ymax]
                window_ids, window_counts = np.unique(s_cells, return_counts=True)
                if 0 in window_ids:
                    window_ids = window_ids[1:]
                    window_counts = window_counts[1:]
                # Calculate fragmentation based on pixel count in moving window
                frag_indi_counts = frag_ind(window_counts)
                
                #calc fragmentation based on orig areas
                df_window = df_rep_subset.loc[df_rep_subset['frag_id'].isin(window_ids)]
                df_window_array = np.array(df_window['area']/(1000*1000)).astype(int)
                frag_indi_orig = frag_ind(df_window_array)
                
                out_count_area[x-100,y-100] = int(frag_indi_counts + .5)
                out_orig_area[x-100,y-100] = int(frag_indi_orig + .5)

    # Write output raster considering pixel counts
    outraster_counts = os.path.join(outpath, "window_count3", os.path.basename(tile)) 
    write_tif(tile,outraster_counts, out_count_area, 1)

    # Write output raster considering original areas
    outraster_orig_area = os.path.join(outpath, "original_area3", os.path.basename(tile))
    write_tif(tile,outraster_orig_area, out_orig_area, 1)


    return 'tile: {} written'.format(tile.split(os.sep))

# Define path input files and and output directory
tile_path = r"S:\eu_fragmentation_forest\result_grass\frag_unique_masked_tr1000"
report_path = r"S:\eu_fragmentation_forest\result_grass\tables\report_unique_areas.file"

# Read report file and process the data 
df_report = pd.read_csv(report_path, sep='|', skiprows=15 ,skipfooter=3, names=['a', 'frag_id', 'b','area','c'], thousands=',', engine='python')
df_report = df_report.loc[:, ['frag_id', 'area']]

outpath = r'S:\eu_fragmentation_forest\result'
log = open(outpath+'\\frag_ind.log', 'w')

# Get list of tiles to process
tiles = glob(tile_path + r'\*.tif')
sur_radius = 5 # Radius of cells for surrounding the center_pixel

if __name__=='__main__':
    pool = Pool(10) # Set the cores depending the capacity of you computer
    for bar in pool.imap_unordered(main, tiles):
        log.write(bar)
        log.flush()

    log.close() 
