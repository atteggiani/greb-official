# Libraries
import sys
import warnings
import os
import numpy as np
from cdo import Cdo
import iris
import iris.coord_categorisation
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import iris.quickplot as qplt
import iris.plot as iplt
import cartopy.crs as ccrs

from climate_module import * # Import self defined classes and function

# Ignore warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")

# Reading file name
filename = sys.argv[1]
# filename = r'~/university/phd/greb-official/output/scenario.exp-230.forced.climatechange.ensemblemean.111'
name = os.path.split(filename)[1]
outfile = filename + '.nc'

# Setting figures output directory
outdir=os.path.join('../figures',name)
os.makedirs(outdir,exist_ok=True)

# Converting bin file to netCDF
print('\nFILENAME: '+ name)
print('Converting binary file to netCDF...')
cdo = Cdo() # Initialize CDO
cdo.import_binary(input = filename+'.ctl', output = outfile, options = '-f nc')

# Importing the data cube
data = iris.load(outfile)
data = parsevar(data)

#  Plotting data countour
print('Saving annual mean contours...')
plot_annual_mean(data,outpath=outdir)
print('Saving seasonal cycle contours...')
plot_seasonal_cycle(data,outpath=outdir)

# Delete netCDF file
print('Deleting netCDF file...')
os.remove(outfile)
print('Done!!')
