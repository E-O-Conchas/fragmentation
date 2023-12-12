# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 12:39:02 2023

@author: no67wuwu
"""

import os
import numpy as np
import pandas as pd
from glob import glob

import MacPyver as mp

from multiprocessing import Pool

# fragmentation function from Aurora
def frag_ind(s):
    area = ((sur_radius*2)+1)**2
    a = map(lambda x: x**2, s)
    a = sum(a)*1.0/area
    return a


# path to files:
tile_path = r"S:\Emmanuel_OcegueraConchas\eu_fragmentation_forest\result_grass\frag_unique_masled_tr1000"


# path to textfile / split the file / result from the grass report function
report_path = r"S:\Emmanuel_OcegueraConchas\eu_fragmentation_forest\result_grass\tables\report_unique_areas.file"
df_report = pd.read_csv(report_path, sep='|', skiprows=15 ,skipfooter=3, names=['a', 'frag_id', 'b','area','c'], thousands=',', engine='python')
df_report = df_report.loc[:, ['frag_id', 'area']]

outpath = r'S:\Emmanuel_OcegueraConchas\eu_fragmentation_forest\result\frag_ind'
log = open(outpath+'\\frag_ind.log', 'w')



def get_tiles(tile):
    ''' get surrounding tiles '''
    name = tile.split(os.sep)[-1]
    y_top = int(name.split('-')[1])-1
    y_bot = y_top + 2
    x_left = int(name.split('-')[2].split('.')[0])-1
    x_right = x_left + 2
    
    #all possible surrounding tiles
    sur_tiles = ['fr_cl_tile-{}-{}.tif'.format(('000'+str(y))[-3:], ('000'+str(x))[-3:]) 
            for y in range(y_top, y_bot+1)  
                for x in range(x_left, x_right+1) ]
     
    #position of the tiles               
    pos_dic_tiles = {}
    pos = ['0,0','0,1','0,2',
           '1,0','1,1','1,2',
           '2,0','2,1','2,2']
           
    pos_count = 0
    for st in sur_tiles:
        pos_dic_tiles[st] = pos[pos_count]
        pos_count +=1
    
    
    #get all existing tiles
    sur_tile_paths = [x for x in tiles for y in sur_tiles if y in x]
    
    # create empty array
    array = np.zeros([300,300])
    array.fill(-1)
    
    # fill array with data
    for stp in sur_tile_paths:
        # get position in merge array
        stp_name = stp.split(os.sep)[-1]
        sub_rast = mp.raster.tiff.read_tif(stp)
        
        # Check the shape of the sub_rast
        if sub_rast.shape != (100, 100):
            print(f"Unexpected shape for {stp_name}: {sub_rast.shape}")
            continue  # Skip this tile or handle the error as needed

        # fill position based on the position dic
        ymin = int(pos_dic_tiles[stp_name].split(',')[0]) * 100
        ymax = ymin +100
        xmin = int(pos_dic_tiles[stp_name].split(',')[1]) * 100
        xmax = xmin + 100
        array[ymin:ymax, xmin:xmax] = sub_rast
    
    return array
    
    # # create empty array
    # array = np.zeros([300,300])
    # array.fill(-1)
    # #fill array with data
    
    # for stp in sur_tile_paths:
    #     #get position in merge array
    #     stp_name = stp.split(os.sep)[-1]
    #     sub_rast = mp.raster.tiff.read_tif(stp)
    #     # fill position based on the position dic
    #     ymin = int(pos_dic_tiles[stp_name].split(',')[0]) * 100
    #     ymax = ymin +100
    #     xmin = int(pos_dic_tiles[stp_name].split(',')[1]) * 100
    #     xmax = xmin + 100
    #     array[ymin:ymax, xmin:xmax] = sub_rast
    
    # return array
    
    
    
def bbox(x,y, sur_radius):
    '''get the bounding box'''
    xmin = x - sur_radius
    xmax = x + sur_radius + 1
    ymin = y - sur_radius
    ymax = y + sur_radius + 1
    return xmin, xmax, ymin, ymax

def main(tile):
    
    # get surrownding tiles
    raster = get_tiles(tile)
    orig_raster = mp.raster.tiff.read_tif(tile)
    out_count_area = np.zeros(orig_raster.shape)
    out_orig_area = np.zeros(orig_raster.shape)
    
    frag_ids = np.unique(raster[:,:]) 
    #frag_ids = np.unique(raster[95:205, 95:205]) 
    frag_ids = np.delete(frag_ids, np.where(frag_ids==0))
    df_rep_subset = df_report.loc[df_report['frag_id'].isin(frag_ids)]
    
    
    for x in range(100,200):
        for y in range(100, 200):
            if raster[x,y]!=0:
                # get surrounding cells
                xmin, xmax, ymin, ymax = bbox(x, y, sur_radius)
                s_cells = raster[ xmin : xmax, ymin : ymax]
                window_ids, window_counts = np.unique(s_cells, return_counts=True)
                if 0 in window_ids:
                    window_ids = window_ids[1:]
                    window_counts = window_counts[1:]
                #calc fragmentation based on pixel count in moving window
                frag_indi_counts = frag_ind(window_counts)
                
                #calc fragmentation based on orig areas
                df_window = df_rep_subset.loc[df_rep_subset['frag_id'].isin(window_ids)]
                df_window_array = np.array(df_window['area']/(1000*1000)).astype(int)
                frag_indi_orig = frag_ind(df_window_array)
                
                
                out_count_area[x-100,y-100] = int(frag_indi_counts + .5)
                out_orig_area[x-100,y-100] = int(frag_indi_orig + .5)

    
    # considering just the pixel in the window    
    outraster_counts = r'S:\Emmanuel_OcegueraConchas\eu_fragmentation_forest\result\window_count3' + os.sep + tile.split(os.sep)[-1]
    mp.raster.tiff.write_tif(tile,outraster_counts, out_count_area, 1)
    # considering the original area from the id    
    outraster_orig_area = r'S:\Emmanuel_OcegueraConchas\eu_fragmentation_forest\result\orig_area3' + os.sep + tile.split(os.sep)[-1]
    mp.raster.tiff.write_tif(tile,outraster_orig_area, out_orig_area, 1)
    return 'tile: {} written'.format(tile.split(os.sep))


tiles = glob(tile_path + '\*.tif')
sur_radius = 5 #radius of cells for surrounding the center_pixel

if __name__=='__main__':
    pool = Pool(20)
    for bar in pool.imap_unordered(main, tiles):
        log.write(bar)
        log.flush()

    log.close() 
