# Libraries
import sys
import os
import numpy as np
from cdo import Cdo
import iris
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import iris.quickplot as qplt
import iris.plot as iplt
import cartopy.crs as ccrs
cdo=Cdo()

# pltvar  = 0 # (0=Tsurf, 1=Tatmos, 2=Tocean, 3=spec. humidity, 4=albedo, 5=precipitation (mm/day), 6=precip (kg m-2 s-1), 7=eva (kg m-2 s-1), 8=crcl (kg m-2 s-1))
pltvar  = ('tsurf', 'tatmos', 'tocean', 'ice', 'spec. humidity', 'albedo', 'precip', 'eva', 'crcl')
units = ('K','K','K','','','','kg m^-2 s^-1','kg m^-2 s^-1','kg m^-2 s^-1')
# Reading file name
# filename = sys.argv[1]
filename = r'~/university/phd/greb-official/output/scenario.exp-230.forced.climatechange.ensemblemean.111'
name = os.path.split(filename)[1]
outfile = filename + '.nc'

# Setting figures output directory
outdir=os.path.join(os.getcwd(),'figures',name)
os.makedirs(outdir,exist_ok=True)

# Converting bin file to netCDF
cdo.import_binary(input = filename+'.ctl',    output = outfile,  options = '-f nc')

# Importing the data cube
data = iris.load(outfile)
varnames=[var.var_name for var in data]
# varnames.index('tatmos')

# Create annual mean
amean=[iris.util.squeeze(var.collapsed('time',iris.analysis.MEAN)) for var in data]
# Create seasonal cycle (DJF-JJA)

# # plot annual mean
# cmap=cm.seismic
# ext = 'png'
# for var in amean:
#     plt.figure(figsize=(12, 8))
#     plt.subplot(111,projection=ccrs.Robinson())
#     iplt.contourf(var, 20,cmap=cmap)
#     # Add coastlines to the map
#     plt.gca().coastlines()
#     plt.colorbar(orientation='horizontal',extend='both')
#     plt.title(var.var_name)
#     outname = '.'.join([var.var_name,'amean',ext])
#     iplt.citation(name)
#     plt.savefig(os.path.join(outdir,outname), format=ext, dpi=300)

# Plot annual mean for 'PRECIP'
ext = 'png'
ind=varnames.index('precip')
var=amean[ind]*-86400
units = 'mm/day'
bound = range(0,12,2)
plt.figure(figsize=(12, 8))
plt.subplot(111,projection=ccrs.Robinson())
iplt.contourf(var, 9,cmap=cm.GnBu)
# Add coastlines to the map
plt.gca().coastlines()
plt.colorbar(orientation='horizontal',extend='both',label = units,
            boundaries=bounds)

plt.title('Precipitation')
iplt.citation(name)
outname = '.'.join(['precip','amean',ext])
plt.savefig(os.path.join(outdir,outname), format=ext, dpi=300)

# Deleting netCDF file after analysis
# os.remove(outfile)

# def parsecvar(varlist):
#     pltvar  = ('tsurf', 'tatmos', 'tocean', 'precip', 'eva', 'crcl')
#     ind = [pltvar.index(var) if var in pltvar else np.nan for var in varlist]
#     # if var not in pltvar:
#     #     Warning("'"+var+"' is not a recognized variable")
#     return ind
#
# # Settings for 'precip'
#     units = 'mm/day'
#     name = 'Precipitation'
#     coeff = 86400
#     bounds = [0,2,4,6,8,10]
