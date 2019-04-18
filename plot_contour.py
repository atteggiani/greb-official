# Libraries
import sys
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
cdo=Cdo()

# FUNCTIONS //==============================================//
def parsevar(cubes):
    # Correct values of output variables
    fl=False
    if not isinstance(cubes,list):
        cubes = [cubes]
        fl=True
    varnames=[var.var_name for var in cubes]
    for var in cubes:
        var.long_name = None
    # PRECIP
    if 'precip' in varnames:
        ind = varnames.index('precip')
        cubes[ind]*=-1
        cubes[ind].var_name='precip'
    return cubes[0] if fl else cubes

def annual_mean(cubes):
    # Create annual mean

    fl=False
    if not isinstance(cubes,list):
        cubes = [cubes]
        fl=True
    # get var names
    varnames=[var.var_name for var in cubes]
    # compute annual mean
    amean=[iris.util.squeeze(var.collapsed('time',iris.analysis.MEAN)) for var in cubes]
    # set var names
    for var,name in zip(amean,varnames):
        var.var_name = name+'.amean'
    return amean[0] if fl else amean

def seasonal_cycle(cubes):
    # Create seasonal cycle (DJF-JJA)

    fl=False
    if not isinstance(cubes,list):
        cubes = [cubes]
        fl=True
    # get var names
    varnames=[var.var_name for var in cubes]
    # add seasons
    [iris.coord_categorisation.add_season(var, 'time', name='seasons', seasons=('djf', 'mam', 'jja', 'son')) for var in cubes]
    # compute seasonal cycle
    seasonmean = [iris.util.squeeze(var.aggregated_by('seasons',iris.analysis.MEAN)) for var in cubes]
    djf = [var.extract(iris.Constraint(seasons='djf')) for var in seasonmean]
    jja = [var.extract(iris.Constraint(seasons='jja')) for var in seasonmean]
    cycle = [var1-var2 for var1,var2 in zip(djf,jja)]
    # set var names
    for var,name in zip(cycle,varnames):
        var.var_name = name+'.seascyc'
    return cycle[0] if fl else cycle

# pltvar  = ('tsurf', 'tatmos', 'tocean', 'precip', 'eva', 'qcrcl')
# units = ('K','K','K','kg m^-2 s^-1','kg m^-2 s^-1','kg m^-2 s^-1')
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
data = parsevar(data)
# varnames=[var.var_name for var in data]

# Create annual mean
amean=annual_mean(data)

# Create seasonal cycle (DJF-JJA)
cycle=seasonal_cycle(data)

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
ind=[var.var_name for var in data].index('precip')
var=amean[ind]*86400
units = 'mm/day'
cmaplev = np.arange(0,12)
cbticks = np.arange(0,12,2)
cmap = cm.GnBu
varname = 'precip'
tit = 'Precipitation'

plt.figure(figsize=(12, 8))
plt.subplot(111,projection=ccrs.Robinson())
iplt.contourf(var, levels = cmaplev, cmap=cmap, extend='both')
plt.gca().coastlines()
plt.colorbar(orientation='horizontal',extend='both',label = units,
            ticks=cbticks)
plt.title(tit)
iplt.citation(name)
outname = '.'.join([varname,'amean',ext])
plt.savefig(os.path.join(outdir,outname), format=ext, dpi=300)

# Plot annual mean for 'EVA'
ext = 'png'
ind=[var.var_name for var in data].index('eva')
var=amean[ind]*86400
units = 'mm/day'
cmaplev = np.arange(-8,9)
cbticks = np.arange(-8,10,2)
cmap = cm.bwr_r
varname = 'eva'
tit = 'Evaporation'

plt.figure(figsize=(12, 8))
plt.subplot(111,projection=ccrs.Robinson())
iplt.contourf(var, levels = cmaplev, cmap=cmap, extend='both')
plt.gca().coastlines()
plt.colorbar(orientation='horizontal',extend='both',label = units,
            ticks=cbticks)
plt.title(tit)
iplt.citation(name)
outname = '.'.join([varname,'amean',ext])
plt.savefig(os.path.join(outdir,outname), format=ext, dpi=300)

# Plot annual mean for 'CRCL'
ext = 'png'
ind=[var.var_name for var in data].index('qcrcl')
var=amean[ind]*86400
units = 'mm/day'
cmaplev = np.arange(-8,9)
cbticks = np.arange(-8,10,2)
cmap = cm.bwr_r
varname = 'qcrcl'
tit = 'Circulation'

plt.figure(figsize=(12, 8))
plt.subplot(111,projection=ccrs.Robinson())
iplt.contourf(var, levels = cmaplev, cmap=cmap, extend='both')
plt.gca().coastlines()
plt.colorbar(orientation='horizontal',extend='both',label = units,
            ticks=cbticks)
plt.title(tit)
iplt.citation(name)
outname = '.'.join([varname,'amean',ext])
plt.savefig(os.path.join(outdir,outname), format=ext, dpi=300)

# ===============================================================
# ===============================================================

# Plot seasonal cycle for 'PRECIP'
ext = 'png'
ind=[var.var_name for var in cycle].index('precip_seascyc')
var=cycle[ind]*86400
units = 'mm/day'
cmaplev = np.arange(-5,6)
cbticks = np.arange(-4,6,2)
cmap = cm.bwr_r
varname = 'precip'
tit = 'Precipitation Seasonal Cycle'
plt.figure(figsize=(12, 8))
plt.subplot(111,projection=ccrs.Robinson())
iplt.contourf(var, levels = cmaplev, cmap=cmap, extend='both')
plt.gca().coastlines()
plt.colorbar(orientation='horizontal',extend='both',label = units,
            ticks=cbticks)
plt.title(tit)
iplt.citation(name)
outname = '.'.join([varname,'seascyc',ext])
plt.savefig(os.path.join(outdir,outname), format=ext, dpi=300)

# Plot seasonal cycle for 'EVA'
ext = 'png'
ind=[var.var_name for var in cycle].index('eva_seascyc')
var=cycle[ind]*86400
units = 'mm/day'
cmaplev = np.arange(-8,9)
cbticks = np.arange(-8,10,2)
cmap = cm.bwr_r
varname = 'eva'
tit = 'Evaporation seasonal cycle'

plt.figure(figsize=(12, 8))
plt.subplot(111,projection=ccrs.Robinson())
iplt.contourf(var, levels = cmaplev, cmap=cmap, extend='both')
plt.gca().coastlines()
plt.colorbar(orientation='horizontal',extend='both',label = units,
            ticks=cbticks)
plt.title(tit)
iplt.citation(name)
outname = '.'.join([varname,'seascyc',ext])
plt.savefig(os.path.join(outdir,outname), format=ext, dpi=300)

# Plot annual mean for 'QCRCL'
ext = 'png'
ind=[var.var_name for var in cycle].index('qcrcl_seascyc')
var=cycle[ind]*86400
units = 'mm/day'
cmaplev = np.arange(-8,9)
cbticks = np.arange(-8,10,2)
cmap = cm.bwr_r
varname = 'qcrcl'
tit = 'Circulation seasonal cycle'

plt.figure(figsize=(12, 8))
plt.subplot(111,projection=ccrs.Robinson())
iplt.contourf(var, levels = cmaplev, cmap=cmap, extend='both')
plt.gca().coastlines()
plt.colorbar(orientation='horizontal',extend='both',label = units,
            ticks=cbticks)
plt.title(tit)
iplt.citation(name)
outname = '.'.join([varname,'seascyc',ext])
plt.savefig(os.path.join(outdir,outname), format=ext, dpi=300)

# Deleting netCDF file after analysis
# os.remove(outfile)

# def parsecvar(varlist):
#     pltvar  = ('tsurf', 'tatmos', 'tocean', 'precip', 'eva', 'qcrcl')
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
