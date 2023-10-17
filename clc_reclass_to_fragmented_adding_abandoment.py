# -*- coding: utf-8 -*-
"""
Created on Wed Feb 06 16:58:17 2019

@author: fw56moba
"""

import numpy as np

import MacPyver as mp


clc_path = r"I:\biocon\GIS_data\Corine_LandCover\g250_clc12_V18_5.tif"
aban_path = r"I:\biocon\Projects\RewildingMAP\DataSources\LandAbandonement\LandAbandonment_Scenarios\A1AbandAr2040_250m_3035.tif"

#read in rasters
clc = mp.raster.tiff.read_tif(clc_path)
aba = mp.raster.tiff.read_tif(aban_path)


# values are the unique values form the column code_12 from the 
#corine landcover shapefile
#using: shp_values = set(row[0] for row in arcpy.da.SearchCursor("clc12_Version_18_5", "code_12"))
shp_values = [u'111', u'112', u'121', u'122', u'123', u'124', u'131', u'132', u'133', u'141',
 u'142', u'211', u'212', u'213', u'221', u'222', u'223', u'231', u'241', u'242',
 u'243', u'244', u'311', u'312', u'313', u'321', u'322', u'323', u'324', u'331',
 u'332', u'333', u'334', u'335', u'411', u'412', u'421', u'422', u'423', u'511',
 u'512', u'521', u'522', u'523', u'999']

#get unique values from clc raster
uniq = np.unique(clc)

#create translation from raster value to code_12 value
clc_dic = {}
for x in range(len(shp_values)): 
    clc_dic[uniq[x]] = int(shp_values[x])

"""result from the dictionary function above:
#dictionary contains the translation from raster value to shape code_12 value
'''
{1: 111, 2: 112, 3: 121, 4: 122, 5: 123, 6: 124, 7: 131, 8: 132, 9: 133,
 10: 141, 11: 142, 12: 211, 13: 212, 14: 213, 15: 221, 16: 222, 17: 223,
 18: 231, 19: 241, 20: 242, 21: 243, 22: 244, 23: 311, 24: 312, 25: 313,
 26: 321, 27: 322, 28: 323, 29: 324, 30: 331, 31: 332, 32: 333, 33: 334,
 34: 335, 35: 411, 36: 412, 37: 421, 38: 422, 39: 423, 40: 511, 41: 512,
 42: 521, 43: 522, 44: 523, 48: 999}
"""

#copy raster
clc_code_12 = clc[:]
#translate raster values based on the dictionary
for x in clc_dic:
    clc_code_12 = np.where(clc_code_12 == x, clc_dic[x], clc_code_12)


#reclass raster pastures as intensive agriculture 
dicti = {'a':[111,113,999], 'b':[211,242,999], 'c':[512, 523, 999], 'd':[995,995,999]}

inraster = clc_code_12[:]
outraster = inraster[:]
for x in dicti:
    start,end,new_value = dicti[x]
    outraster = np.where((inraster>=start)&(inraster<=end),new_value, outraster )

#translate all values to 1 which are not 999 or 255
outraster = np.where((outraster != 999) & (outraster != 255), 1, outraster)

#add abandomant area to landcover
outraster = np.where(aba == 1, 1, outraster)

#save to tif file
mp.raster.tiff.write_tif(clc_path, r'O:\GIS_data\Corine_LandCover\g250_clc12_V18_5_reclass_binar_02.tif', outraster, 0, nodata = 255, option = "COMPRESS=DEFLATE")


outraster = np.where(outraster==999, 9, outraster)
outraster = np.where(clc == 44, 0, outraster)
outraster = np.where(outraster==255,0,outraster)
mp.raster.tiff.write_tif(clc_path,  r'I:\biocon\Emmanuel_Oceguera\projects\2023_03_NaturaConnect\dataSources\clc2018_v2020_geoPackage_Raster\g250_clc12_V18_5_reclass_binar_excl_abandom_8bit.tif',outraster, 6, nodata=0, option="COMPRESS=DEFLATE")


"""
Continue in arcmap 
convert raster to polygon
"""