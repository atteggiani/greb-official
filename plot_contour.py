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

# Ignore warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")

# CLASSES and FUNCTIONS //==============================================//
def annual_mean(cubes):
    # Create annual mean
    fl=False
    if not isinstance(cubes,list):
        cubes = [cubes]
        fl=True
    # get var names
    varnames=[var.var_name for var in cubes]
    # compute annual mean
    amean=[iris.util.squeeze(var.collapsed('time',iris.analysis.MEAN)) \
                                                            for var in cubes]
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
    [iris.coord_categorisation.add_season(var, 'time', name='seasons',
     seasons=('djf', 'mam', 'jja', 'son')) for var in cubes if \
     'seasons' not in [coord.name() for coord in var.coords()]]
    # compute seasonal cycle
    seasonmean = [iris.util.squeeze(var.aggregated_by('seasons',
                                        iris.analysis.MEAN)) for var in cubes]
    djf = [var.extract(iris.Constraint(seasons='djf')) for var in seasonmean]
    jja = [var.extract(iris.Constraint(seasons='jja')) for var in seasonmean]
    cycle = [var1-var2 for var1,var2 in zip(djf,jja)]
    # set var name
    for var,name in zip(cycle,varnames):
        var.var_name = name+'.seascyc'
    return cycle[0] if fl else cycle

class plot_param:
    ext = 'png'
    def __init__(self, cube = None, units = None, cmap = None, cmaplev = None,
                 cbticks = None, defname = None, varname = None, tit = None):
        self.cube = cube
        self.cmap = cmap
        self.cmaplev = cmaplev
        self.cbticks = cbticks
        self.units = units
        self.defname = defname
        self.varname = varname
        self.tit = tit

    def __str__(self):
        return str(print(self.cube))

    def set_cube(self,cube):
        self.cube = cube

    def set_units(self,units):
        self.units = units

    def set_cmap(self,cmap):
        self.cmap = cmap

    def set_cmaplev(self,cmaplev):
        self.cmaplev = cmaplev

    def set_cbticks(self,cbticks):
        self.cbticks = cbticks

    def set_varname(self,varname):
        self.varname = varname

    def set_tit(self,tit):
        self.tit = tit

    def get_cube(self):
        return self.cube

    def get_units(self):
        return self.units

    def get_cmap(self):
        return self.cmap

    def get_cmaplev(self):
        return self.cmaplev

    def get_cbticks(self):
        return self.cbticks

    def get_defname(self):
        return self.defname

    def get_varname(self):
        return self.varname

    def get_tit(self):
        return self.tit

    def plot(self, outpath = None, dpi = 300):
        plt.figure(figsize=(12, 8))
        plt.subplot(111,projection=ccrs.Robinson())
        iplt.contourf(self.cube, levels = self.cmaplev, cmap = self.cmap,
                      extend='both')
        plt.gca().coastlines()
        plt.colorbar(orientation='horizontal',extend='both',label = self.units,
                    ticks = self.cbticks)
        plt.title(self.tit)
        # iplt.citation(name)
        if outpath is not None:
            plt.savefig(os.path.join(outpath,'.'.join([self.varname,self.ext])),
                        format = self.ext, dpi = dpi)

    @classmethod
    def set_ext(cls,ext):
        cls.ext = ext

    @classmethod
    def from_cube(cls, cube, units = None, cmap = cm.RdBu, cmaplev = None,
                  cbticks = None, varname = None, tit = None):
        units = cube.units if units is None else units
        cmaplev = cmap.N if cmaplev is None else cmaplev
        varname = cube.var_name if varname is None else varname
        tit = cube.var_name if tit is None else tit

        return cls(cube = cube, units = units, cmap = cmap, cmaplev = cmaplev,
                   cbticks = cbticks, defname = cube.var_name,
                   varname = varname, tit = tit)
    @classmethod
    def annual_mean(cls, cube, units = None, cmap = cm.RdBu, cmaplev = None,
                  cbticks = None, varname = None, tit = None):
        defname = cube.var_name
        cube = annual_mean(cube)
        units = cube.units if units is None else units
        cmaplev = cmap.N if cmaplev is None else cmaplev
        varname = cube.var_name if varname is None else varname
        tit = cube.var_name if tit is None else tit

        return cls(cube = cube, units = units, cmap = cmap, cmaplev = cmaplev,
                   cbticks = cbticks, defname = defname, varname = varname,
                   tit = tit)

    @classmethod
    def seasonal_cycle(cls, cube, units = None, cmap = cm.RdBu, cmaplev = None,
                       cbticks = None, varname = None, tit = None):
        defname = cube.var_name
        cube = seasonal_cycle(cube)
        units = cube.units if units is None else units
        cmaplev = cmap.N if cmaplev is None else cmaplev
        varname = cube.var_name if varname is None else varname
        tit = cube.var_name if tit is None else tit

        return cls(cube = cube, units = units, cmap = cmap, cmaplev = cmaplev,
                   cbticks = cbticks, defname = defname, varname = varname,
                   tit = tit)

    def to_annual_mean(self):
        tit = self.get_tit()
        cube = self.get_cube()
        newcube = annual_mean(cube)
        self.set_cube(newcube)
        self.set_varname(newcube.var_name)
        if newcube.var_name == tit + '.amean':
            self.set_tit(newcube.var_name)
        else: self.set_tit(tit)
        return self

    def to_seasonal_cycle(self):
        tit = self.get_tit()
        cube = self.get_cube()
        newcube = seasonal_cycle(cube)
        self.set_cube(newcube)
        self.set_varname(newcube.var_name)
        if newcube.var_name == tit + '.seascyc':
            self.set_tit(newcube.var_name)
        else: self.set_tit(tit)
        return self

def parsevar(cubes):
    # Initialize output variables
    fl=False
    if not isinstance(cubes,list):
        cubes = [cubes]
        fl=True
    varnames=[var.var_name for var in cubes]
    for var in cubes:
        var.long_name = None
    # PRECIP
    id = 'precip'
    if id in varnames:
        ind = varnames.index(id)
        cubes[ind]*=-1*86400
        cubes[ind].var_name=id
        cubes[ind].units='mm/day'
    # EVA
    id = 'eva'
    if id in varnames:
        ind = varnames.index(id)
        cubes[ind]*=86400
        cubes[ind].var_name=id
        cubes[ind].units='mm/day'
    # QCRCL
    id = 'qcrcl'
    if id in varnames:
        ind = varnames.index(id)
        cubes[ind]*=86400
        cubes[ind].var_name=id
        cubes[ind].units='mm/day'
    # TSURF
    id = 'tsurf'
    if id in varnames:
        ind = varnames.index(id)
        cubes[ind].units='K'
    # TATMOS
    id = 'tatmos'
    if id in varnames:
        ind = varnames.index(id)
        cubes[ind].units='K'
    # TOCEAN
    id = 'tocean'
    if id in varnames:
        ind = varnames.index(id)
        cubes[ind].units='K'
    return cubes[0] if fl else cubes

def plot_annual_mean(cubes,outpath=None):
    # Initialize output variables
    fl=False
    if not isinstance(cubes,list):
        cubes = [cubes]
        fl=True
    varnames=[var.var_name for var in cubes]
    txt = ' Annual Mean'
    # TSURF
    id = 'tsurf'
    if id in varnames:
        ind = varnames.index(id)
        plot_param.from_cube(cube = cubes[ind], cmap = cm.RdBu_r,
                             cmaplev = np.arange(213,333+5,5),
                             cbticks = np.arange(213,333+10,10),
                             tit = 'Surface Temperature'+txt). \
                             to_annual_mean().plot(outpath)
    # TATMOS
    id = 'tatmos'
    if id in varnames:
        ind = varnames.index(id)
        plot_param.from_cube(cube = cubes[ind], cmap = cm.RdBu_r,
                             cmaplev = np.arange(213,333+5,5),
                             cbticks = np.arange(213,333+10,10),
                             tit = 'Atmospheric Temperature'+txt). \
                             to_annual_mean().plot(outpath)
    # TOCEAN
    id = 'tocean'
    if id in varnames:
        ind = varnames.index(id)
        plot_param.from_cube(cube = cubes[ind], cmap = cm.Reds,
                             cmaplev = np.arange(273,323+5,5),
                             cbticks = np.arange(273,333+10,10),
                             tit = 'Ocean Temperature'+txt). \
                             to_annual_mean().plot(outpath)
    # PRECIP
    id = 'precip'
    if id in varnames:
        ind = varnames.index(id)
        plot_param.from_cube(cube = cubes[ind], cmap = cm.GnBu,
                             cmaplev = np.arange(0,15),
                             cbticks = np.arange(0,17,2),
                             tit = 'Precipitation'+txt). \
                             to_annual_mean().plot(outpath)
    # EVA
    id = 'eva'
    if id in varnames:
        ind = varnames.index(id)
        plot_param.from_cube(cube = cubes[ind],
                             cmaplev = np.arange(-8,9),
                             cbticks = np.arange(-8,10,2),
                             tit = 'Evaporation'+txt). \
                             to_annual_mean().plot(outpath)
    # QCRCL
    id = 'qcrcl'
    if id in varnames:
        ind = varnames.index(id)
        plot_param.from_cube(cube = cubes[ind],
                             cmaplev = np.arange(-8,9),
                             cbticks = np.arange(-8,10,2),
                             tit = 'Circulation'+txt). \
                             to_annual_mean().plot(outpath)

def plot_seasonal_cycle(cubes,outpath=None):
    # Initialize output variables
    fl=False
    if not isinstance(cubes,list):
        cubes = [cubes]
        fl=True
    varnames=[var.var_name for var in cubes]
    txt = ' Seasonal Cycle'
    # TSURF
    id = 'tsurf'
    if id in varnames:
        ind = varnames.index(id)
        plot_param.from_cube(cube = cubes[ind], cmap = cm.RdBu_r, units = '°C',
                             cmaplev = np.arange(-50,50+5,5),
                             cbticks = np.arange(-50,50+10,10),
                             tit = 'Surface Temperature'+txt). \
                             to_seasonal_cycle().plot(outpath)
    # TATMOS
    id = 'tatmos'
    if id in varnames:
        ind = varnames.index(id)
        plot_param.from_cube(cube = cubes[ind], cmap = cm.RdBu_r, units = '°C',
                             cmaplev = np.arange(-50,50+5,5),
                             cbticks = np.arange(-50,50+10,10),
                             tit = 'Atmospheric Temperature'+txt). \
                             to_seasonal_cycle().plot(outpath)
    # TOCEAN
    id = 'tocean'
    if id in varnames:
        ind = varnames.index(id)
        plot_param.from_cube(cube = cubes[ind], cmap = cm.RdBu_r, units = '°C',
                             cmaplev = np.arange(-0.35,0.35+0.05,0.05),
                             cbticks = np.arange(-0.35,0.35+0.05,0.1),
                             tit = 'Ocean Temperature'+txt). \
                             to_seasonal_cycle().plot(outpath)
    # PRECIP
    id = 'precip'
    if id in varnames:
        ind = varnames.index(id)
        plot_param.from_cube(cube = cubes[ind],
                             cmaplev = np.arange(-10,11),
                             cbticks = np.arange(-10,10+2,2),
                             tit = 'Precipitation'+txt). \
                             to_seasonal_cycle().plot(outpath)
    # EVA
    id = 'eva'
    if id in varnames:
        ind = varnames.index(id)
        plot_param.from_cube(cube = cubes[ind],
                             cmaplev = np.arange(-10,11),
                             cbticks = np.arange(-10,10+2,2),
                             tit = 'Evaporation'+txt). \
                             to_seasonal_cycle().plot(outpath)
    # QCRCL
    id = 'qcrcl'
    if id in varnames:
        ind = varnames.index(id)
        plot_param.from_cube(cube = cubes[ind],
                             cmaplev = np.arange(-10,11),
                             cbticks = np.arange(-10,10+2,2),
                             tit = 'Circulation'+txt). \
                             to_seasonal_cycle().plot(outpath)
# /============================================================================/
# CODE
# /============================================================================/

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
