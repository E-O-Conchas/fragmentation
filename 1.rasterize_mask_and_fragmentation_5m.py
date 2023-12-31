# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 10:05:00 2023

@author: no67wuwu

This script is used to rasterize a shapefile that has been imported to a PostGIS database.
It produces two output rasters: a mask and a fragmentation raster.

"""


# Import libraries
import os
import subprocess
from multiprocessing import Pool


def get_stdout(cmd, verbose=False):
    
    """
    Send a command to the command line and fetch the return.
    
    :param cmd: The command to be executed
    :param verbose: Whether to print the command's output
    :return: The command's standard output
    
    from http://blog.kagesenshi.org/2008/02/teeing-python-subprocesspopen-output.html
    """
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = []
    while True:
        line = p.stdout.readline()
        line = line.decode('utf-8') # Decode the bytes into a string
        line = line.replace('\n','').replace('\r','')
        if line != '':
            stdout.append(line)
        if verbose:
            print(line),
        if line == '' and p.poll() != None: #p.poll is checking if the process is still running 
                                            #is it is running it returns None
            break
    return stdout


# Define a function to execute a GDAL command and log the result
def execute_gdal_command(cmd, description, verbose=False):
    """
    Execute a GDAL command and log the result.
    
    :param cmd: The GDAL command to be executed
    :param description: A description of the command
    :param verbose: Whether to print the command's output
    :return: The command's standard output
    """
    print(f"Executing {description}...")
    result = get_stdout(cmd, verbose)
    print(f"{description} completed.")
    return result


# Define the main function
def main(sbbox):
    """
    Main function to rasterize a sub-bounding box.
    
    :param sbbox: The sub-bounding box coordinates (xmin, ymin, xmax, ymax)
    """
    # Extract the extent coordinates
    xmin, ymin, xmax, ymax = sbbox
    
    # Define output file names for mask and fragmentation rasters
    outname_mask = outpath_mask + '\\mask_tile_x{0}_y{1}_1.tif'.format(int(xmin/10000), int(ymin/10000))
    outname_frag = outpath_frag + '\\frag_tile_x{0}_y{1}_1.tif'.format(int(xmin/10000), int(ymin/10000))
    
    # Define GDAL command for fragmentation rasterization
    cmd_frag = """gdal_rasterize -tr 5 5 -co "COMPRESS=DEFLATE" -burn 9 -ot Byte -te {0} {1} {2} {3} \
        -sql "select st_intersection(f.geom, st_geomfromtext('POLYGON (({0} {1}, {2} {1}, {2} {3}, {0} {3}, {0} {1}))', 3035)), \
        f.frag_code, f.id from fragmentation.estonia_forest f where \
        st_intersects(f.geom, st_geomfromtext('POLYGON (({0} {1}, {2} {1}, {2} {3}, {0} {3}, {0} {1}))', 3035)) \
        and f.frag_code = 999"\
        PG:"host=localhost user=postgres dbname=NaturaConnect-Connectivity password=07089452" {4}""".format(xmin, ymin, xmax, ymax, outname_frag)
    
    # Define GDAL command for mask rasterization
    cmd_mask = """gdal_rasterize -tr 5 5 -co "COMPRESS=DEFLATE" -burn 1 -ot Byte -te {0} {1} {2} {3} \
        -sql "select st_intersection(f.geom, st_geomfromtext('POLYGON (({0} {1}, {2} {1}, {2} {3}, {0} {3}, {0} {1}))',3035)), \
        f.id from fragmentation.mask_estonia f where \
        st_intersects(f.geom, st_geomfromtext('POLYGON (({0} {1}, {2} {1}, {2} {3}, {0} {3}, {0} {1}))', 3035))" \
        PG:"host=localhost user=postgres dbname=NaturaConnect-Connectivity password=07089452" {4}""".format(xmin, ymin, xmax, ymax, outname_mask)
    
    # Print the SQL query for fragmentation rasterization
    print("Fragmentation SQL Query:")
    print(cmd_frag)

    # Print the SQL query for mask rasterization
    print("Mask SQL Query:")
    print(cmd_mask)
    
    # Execute GDAL commands for rasterization
    execute_gdal_command(cmd_frag, "Fragmentation Rasterization")
    execute_gdal_command(cmd_mask, "Mask Rasterization")
    

# Define the path to the input shapefile and output paths for mask and fragmentation rasters
inshape = r"I:\biocon\Emmanuel_Oceguera\projects\2023_09_Fragmentation\data\mask\estonia_10km.shp" # to get the extent
outpath_frag = r"I:\biocon\Emmanuel_Oceguera\projects\2023_09_Fragmentation\estonia_forest_fragmentation\frag_raster"
outpath_mask  =  r"I:\biocon\Emmanuel_Oceguera\projects\2023_09_Fragmentation\estonia_forest_fragmentation\land_raster"

# Define a command to get the total extent of the shapefile
cmd = 'ogrinfo -al -so ' + inshape    
    

# Get the total extent of the shapefile
bbox = [x for x in get_stdout(cmd) if x.startswith('Extent')][0]
bbox = bbox.replace('Extent: ','').replace('(','').replace(')','').split(' - ')
bbox = [float(z) for x in bbox for z in x.split(',')]

x_range = bbox[2] - bbox[0]
y_range = bbox[3] - bbox[1]

xmin = bbox[0]
ymin = bbox[1]

    
    
# Create a list of sub-bounding boxes covering the entire extent
sub_bbox_L = []
for x in range(0, int(x_range/100000 + .5)):
    for y in range(0, int(y_range/100000 + .5)):
        sub_bbox_L.append([xmin + 100000 * x, ymin + 100000 * y, xmin + 100000 * (x + 1), ymin + 100000 * (y + 1) ])


# Run the main function over all sub-bounding boxes using multiprocessing
if __name__ == "__main__":
    pool = Pool(10)
    for foo in pool.imap_unordered(main, sub_bbox_L):
        bar = 1

    

    
    
    
    
    
    
    
    
    
    