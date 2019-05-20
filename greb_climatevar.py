# Libraries
import sys
import warnings
import os
import numpy as np
import iris
from cdo import Cdo
import iris.coord_categorisation
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import iris.quickplot as qplt
import iris.plot as iplt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def get_art_cloud_filename(filename):
    txt='exp-930.geoeng.'
    if txt in filename:
        art_cloud_name = filename[filename.index(txt)+len(txt):]
        return os.path.join('/Users/dmar0022/university/phd/greb-official/artificial_clouds',
                           art_cloud_name)
    else:
       return None

def input_file(filename,argv=1):
    if (argv < 1 or not isinstance(argv,int)): raise Exception('argv must be an integer greater than 0')
    try:
        input=sys.argv[argv]
        if ((argv == 1 and input == '-f') or (argv==2 and os.path.splitext(input)[1]=='.json')):
            return rmext(filename)
        else:
            return rmext(input)
    except(IndexError): return rmext(filename)

def plot_artificial_clouds(filename,outpath=None):
    filename = rmext(filename)
    name=os.path.split(filename)[1]
    if outpath is None:
        outpath = '/Users/dmar0022/university/phd/greb-official/'+\
                  'artificial_clouds/art_clouds_figures'
        os.makedirs(outpath,exist_ok=True)
    else:
        if outpath: os.makedirs(outpath,exist_ok=True)
        else: outpath = None
    bin2netCDF(filename)
    data=iris.util.squeeze(iris.load_cube(filename+'.nc'))
    plot_param.from_cube(data[0,:,:],cmap=cm.Greys_r, varname = name,
    cmaplev = np.arange(0,1+0.05,0.05),units = '',
    cbticks = np.arange(0,1+0.1,0.1)).plot(outpath = outpath,
                        coast_param = {'edgecolor':[0,.5,0.3]},statistics=False)
    os.remove(filename+'.nc')

def ignore_warnings():
    # Ignore warnings
    if not sys.warnoptions:
        warnings.simplefilter("ignore")

def data_from_input(filename):
    filename = rmext(filename)
    with open(filename+'.ctl','r') as f:
        a=f.read().split()
    ind=a.index('vars')
    dt = int(a[a.index('tdef')+1])
    dx = int(a[a.index('xdef')+1])
    dy = int(a[a.index('ydef')+1])
    if a[ind+1] != '1': raise Exception('Input with more than one '+\
                                     'variable not yet readable with this function')
    key=[a[ind+2]]
    with open(filename+'.bin','rb') as f:
        val=[np.fromfile(f,dtype=np.float32).reshape(dt,dy,dx).transpose(0,2,1)]
    return dict(zip(key,val))

def rmext(filename):
    path,ext = os.path.splitext(filename)
    if ext not in ['.ctl','.bin','.']: path = path+ext
    return path

def create_bin(path,vars):
    path = rmext(path)
    with open(path+'.bin','wb') as f:
        for v in vars: f.write(v)

def create_ctl(path, varnames = ['clouds'], xdef = 96, ydef = 48, zdef = 1,
               tdef = 730):
    path = rmext(path)
    nvars = len(varnames)
    name = os.path.split(path)[1]+'.bin'
    with open(path+'.ctl','w+') as f:
        f.write('dset ^{}\n'.format(name))
        f.write('undef 9.e27\n')
        f.write('xdef  {} linear 0 3.75\n'.format(xdef))
        f.write('ydef  {} linear -88.125 3.75\n'.format(ydef))
        f.write('zdef   {} linear 1 1\n'.format(zdef))
        f.write('tdef {} linear 00:00Z1jan2000  12hr\n'.format(tdef))
        f.write('vars {}\n'.format(nvars))
        for v in varnames:
            f.write('{0}  1 0 {0}\n'.format(v))
        f.write('endvars\n')

def create_bin_ctl(path,vars):
    if not isinstance(vars,dict):
        raise Exception('vars must be a Dictionary type in the form: ' +
                        '{"namevar1":var1,"namevar2":var2,...,"namevarN":varN}')
    varnames = list(vars.keys())
    nvars = len(varnames)
    varvals = list(vars.values())
    l=[v.shape for v in varvals]
    if not ( l.count(l[0]) == len(l) ):
        raise Exception('var1,var2,...,varN must be of the same size')
    if len(l[0]) != 3:
        raise Exception('create_bin_ctl funcion supports only 2D (tdef x ydef x xdef) time series')
    if 730 not in l[0]:
        raise Exception('tdef must be 730')
    if 96 not in l[0]:
        raise Exception('xdef must be 96')
    if 48 not in l[0]:
        raise Exception('ydef must be 48')
    dt=l[0].index(730)
    dx=l[0].index(96)
    dy=l[0].index(48)
    if not (l[0][0]==730 and l[0][1]==48):
        varvals = [v.transpose(dt,dy,dx) for v in varvals]
    varvals=[np.float32(v.copy(order='C')) for v in varvals]
    # WRITE CTL FILE
    create_ctl(path, varnames = varnames)
    # WRITE BIN FILE
    create_bin(path,vars = varvals)

def bin2netCDF(file):
    filename = rmext(file)
    cdo = Cdo() # Initialize CDO
    cdo.import_binary(input = filename+'.ctl', output = filename+'.nc',
                      options = '-f nc')
def check_bin(filename):
    filename = rmext(filename)
    return os.path.isfile(filename+'.bin')

def check_control(scenario_file):
    path,name = os.path.split(scenario_file)
    if name[:8] == 'scenario':
        name = 'control'+name[8:]
        newfile = os.path.join(path,name)
    else: raise Exception('Input file does not match "scenario" file name')
    return check_bin(newfile),newfile

def check_scenario(control_file):
    path,name = os.path.split(control_file)
    if name[:7] == 'control':
        name = 'scenario'+name[7:]
        newfile = os.path.join(path,name)
    else: raise Exception('Input file does not match "control" file name')
    return check_bin(newfile),newfile

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
    cycle = [(var1-var2)/2 for var1,var2 in zip(djf,jja)]
    # set var name
    for var,name in zip(cycle,varnames):
        var.var_name = name+'.seascyc'
    return cycle[0] if fl else cycle

def difference(cubes,cubes_base):
    fl=False
    if not isinstance(cubes,list):
        cubes = [cubes]
        fl=True
    if not isinstance(cubes_base,list): cubes_base = [cubes_base]
    # get var names
    varnames=[var.var_name for var in cubes]
    varnames_base=[var.var_name for var in cubes_base]
    # compute difference between same variables
    diff = []
    for i,var in enumerate(varnames):
        if var in varnames_base:
            ind = varnames_base.index(var)
            d = cubes[i]-cubes_base[ind]
            d.var_name = cubes[i].var_name
            diff.append(d)
    return diff[0] if fl else diff

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
        cubes[ind].units=''
    # TATMOS
    id = 'tatmos'
    if id in varnames:
        ind = varnames.index(id)
        cubes[ind].units=''
    # TOCEAN
    id = 'tocean'
    if id in varnames:
        ind = varnames.index(id)
        cubes[ind].units=''
    return cubes[0] if fl else cubes

class plot_param:
    ext = 'png'
    defvar = ['tatmos','tsurf','tocean','precip','eva','qcrcl','vapor','ice']

    def __init__(self, cube = None, units = None, cmap = None, cmaplev = None,
                 cbticks = None, cbextmode = None, defname = None,
                 varname = None, tit = None, flag = None):

        self.cube = cube
        self.cmap = cmap
        self.cmaplev = cmaplev
        self.cbticks = cbticks
        self.cbextmode = cbextmode
        self.units = units
        self.defname = defname
        self.varname = varname
        self.tit = tit
        self.flag = flag

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

    def set_cbextmode(self,cbextmode):
        self.cbextmode = cbextmode

    def set_varname(self,varname):
        self.varname = varname

    def set_tit(self,tit):
        self.tit = tit

    def set_flag(self,flag):
        self.flag = flag

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

    def get_cbextmode(self):
        return self.cbextmode

    def get_varname(self):
        return self.varname

    def get_tit(self):
        return self.tit

    def get_flag(self):
        return self.flag

    def plot(self, outpath = None, ax = None, projection = ccrs.Robinson(),
             coast_param = {},
             land_param = {'edgecolor':'face', 'facecolor':'black'},
             title_param = {},
             save_param = {'dpi':300, 'bbox_inches':'tight'},
             statistics=True):
        # plt.figure(figsize=(12, 8))
        plt.axes(projection=projection) if ax is None else plt.axes(ax)
        iplt.contourf(self.get_cube(), levels = self.get_cmaplev(), cmap = self.get_cmap(),
                      extend=self.get_cbextmode())
        plt.gca().add_feature(cfeature.COASTLINE,**coast_param)
        if self.get_defname() == 'tocean':
            plt.gca().add_feature(cfeature.NaturalEarthFeature('physical',
                           'land', '110m', **land_param))
        plt.colorbar(orientation='horizontal',extend = self.get_cbextmode(),
                     label = self.get_units(), ticks = self.get_cbticks())
        plt.title(self.get_tit(),**title_param)
        if statistics:
            txt = 'gmean = {:.3f}\nsp_std = {:.3f}'.format(self.gmean(),self.std_spatial())
            plt.text(1.05,1,txt,verticalalignment='top',horizontalalignment='right',
                     transform=plt.gca().transAxes,fontsize=6)
        if outpath is not None:
            plt.savefig(os.path.join(outpath,'.'.join([self.get_varname(),
                        self.get_ext()])),  format = self.get_ext(),**save_param)

    @classmethod
    def get_ext(cls):
        return cls.ext

    @classmethod
    def get_defvar(cls):
        return cls.defvar

    @classmethod
    def set_ext(cls,ext):
        cls.ext = ext

    @classmethod
    def set_defvar(cls,vars):
        cls.defvar = vars

    @classmethod
    def add_defvar(cls,vars):
        if not isinstance(vars,list):
            vars = [vars]
        cls.set_defvar(cls.get_defvar()+vars)

    @classmethod
    def from_cube(cls, cube, units = None, cmap = cm.RdBu_r, cmaplev = None,
                  cbticks = None, cbextmode = 'neither', varname = None,
                  tit = None):
        units = cube.units if units is None else units
        cmaplev = cmap.N if cmaplev is None else cmaplev
        varname = cube.var_name if varname is None else varname
        tit = cube.var_name if tit is None else tit

        return cls(cube = cube, units = units, cmap = cmap, cmaplev = cmaplev,
                   cbticks = cbticks, cbextmode = cbextmode,
                   defname = cube.var_name, varname = varname, tit = tit)

    def to_annual_mean(self):
        tit = self.get_tit()
        cube = self.get_cube()
        newcube = annual_mean(cube)
        self.set_cube(newcube)
        self.set_varname(newcube.var_name)
        if tit is None:
            self.set_tit(self.get_varname()+'.amean')
        self.set_flag('amean')
        return self

    def to_seasonal_cycle(self):
        tit = self.get_tit()
        cube = self.get_cube()
        newcube = seasonal_cycle(cube)
        self.set_cube(newcube)
        self.set_varname(newcube.var_name)
        if tit is None:
            self.set_tit(self.get_varname()+'.seascyc')
        self.set_flag('seascyc')
        return self

    def to_difference(self,cube_base):
        fl = self.get_flag()
        varname = self.get_varname()
        cube = self.get_cube()
        if fl == 'amean':
            cube_base = annual_mean(cube_base)
        elif fl == 'seascyc':
            cube_base = seasonal_cycle(cube_base)
        newcube = difference(cube,cube_base)
        self.set_cube(newcube)
        self.set_varname(varname)
        return self

    def gmean(self):
        return self.get_cube().data.mean()

    def std_spatial(self):
        return self.get_cube().data.std()

class plot_absolute(plot_param):
    def tatmos(self):
        flag = self.get_flag()
        self.set_units('[K]')
        self.set_cbextmode('both')
        self.set_cmap(cm.RdBu_r)
        if self.get_flag() == 'amean':
            self.set_varname('tatmos.amean')
            self.set_cmaplev(np.arange(223,323+5,5))
            self.set_cbticks(np.arange(223,323+10,10))
            self.set_tit('Atmospheric Temperature Annual Mean')
        elif self.get_flag() == 'seascyc':
            self.set_varname('tatmos.seascyc')
            self.set_cmaplev(np.arange(-20,20+2,2))
            self.set_cbticks(np.arange(-20,20+4,4))
            self.set_tit('Atmospheric Temperature Seasonal Cycle')
        else:
            self.set_varname('tatmos')
            self.set_cmaplev(12)
            self.set_tit('Atmospheric Temperature')
        return self

    def tsurf(self):
        flag = self.get_flag()
        self.set_units('[K]')
        self.set_cbextmode('both')
        self.set_cmap(cm.RdBu_r)
        if flag == 'amean':
            self.set_varname('tsurf.amean')
            self.set_cmaplev(np.arange(223,323+5,5))
            self.set_cbticks(np.arange(223,323+10,10))
            self.set_tit('Surface Temperature Annual Mean')
        elif flag == 'seascyc':
            self.set_varname('tsurf.seascyc')
            self.set_cmaplev(np.arange(-20,20+2,2))
            self.set_cbticks(np.arange(-20,20+4,4))
            self.set_tit('Surface Temperature Seasonal Cycle')
        else:
            self.set_varname('tsurf')
            self.set_cmaplev(12)
            self.set_tit('Surface Temperature')
        return self

    def tocean(self):
        flag = self.get_flag()
        self.set_units('[K]')
        self.set_cbextmode('both')
        self.set_cmap(cm.RdBu_r)
        if self.get_flag() == 'amean':
            self.set_varname('tocean.amean')
            self.set_cmaplev(np.arange(273,303+5,3))
            self.set_cbticks(np.arange(273,303+10,3))
            self.set_tit('Ocean Temperature Annual Mean')
        elif flag == 'seascyc':
            self.set_varname('tocean.seascyc')
            self.set_cmaplev(np.arange(-1,1+1e-1,1e-1))
            self.set_cbticks(np.arange(-1,1+2e-1,2e-1))
            self.set_tit('Ocean Temperature Seasonal Cycle')
        else:
            self.set_varname('tocean')
            self.set_cmaplev(12)
            self.set_tit('Ocean Temperature')
        return self

    def precip(self):
        flag = self.get_flag()
        self.set_units('[mm][day-1]')
        if self.get_flag() == 'amean':
            self.set_varname('precip.amean')
            self.set_cmap(cm.GnBu)
            self.set_cmaplev(np.arange(0,9+1,1))
            self.set_cbticks(np.arange(0,9+1,1))
            self.set_cbextmode('max')
            self.set_tit('Precipitation Annual Mean')
        elif flag == 'seascyc':
            self.set_varname('precip.seascyc')
            self.set_cmap(cm.RdBu_r)
            self.set_cmaplev(np.arange(-6,6+1,1))
            self.set_cmaplev(np.arange(-6,6+1,1))
            self.set_cbextmode('both')
            self.set_tit('Precipitation Seasonal Cycle')
        else:
            self.set_varname('precip')
            self.set_cmap(cm.GnBu)
            self.set_cmaplev(12)
            self.set_cbextmode('both')
            self.set_tit('Precipitation')
        return self

    def eva(self):
        flag = self.get_flag()
        self.set_units('[mm][day-1]') # ADD UNITS!
        if self.get_flag() == 'amean':
            self.set_varname('eva.amean')
            self.set_cmap(cm.Blues)
            self.set_cmaplev(np.arange(0,10+1,1))
            self.set_cbticks(np.arange(0,10+1,1))
            self.set_cbextmode('max')
            self.set_tit('Evaporation Annual Mean')
        elif flag == 'seascyc':
            self.set_varname('eva.seascyc')
            self.set_cmap(cm.RdBu_r)
            self.set_cmaplev(np.arange(-3,3+0.5,0.5))
            self.set_cbticks(np.arange(-3,3+0.5,0.5))
            self.set_cbextmode('both')
            self.set_tit('Evaporation Seasonal Cycle')
        else:
            self.set_varname('eva')
            self.set_cmap(cm.Blues)
            self.set_cmaplev(12)
            self.set_cbextmode('both')
            self.set_tit('Evaporation')
        return self

    def qcrcl(self):
        flag = self.get_flag()
        self.set_units('[mm][day-1]')
        self.set_cbextmode('both')
        self.set_cmap(cm.RdBu_r)
        if self.get_flag() == 'amean':
            self.set_varname('qcrcl.amean')
            self.set_cmaplev(np.arange(-8,8+1))
            self.set_cbticks(np.arange(-8,8+2,2))
            self.set_tit('Circulation Annual Mean')
        elif flag == 'seascyc':
            self.set_varname('qcrcl.seascyc')
            self.set_cmaplev(np.arange(-6,6+1,1))
            self.set_cmaplev(np.arange(-6,6+1,1))
            self.set_tit('Circulation Seasonal Cycle')
        else:
            self.set_varname('qcrcl')
            self.set_cmaplev(12)
            self.set_tit('Circulation')
        return self

    def vapor(self):
        flag = self.get_flag()
        self.set_units(' ') # ADD UNITS!
        if self.get_flag() == 'amean':
            self.set_varname('vapor.amean')
            self.set_cmap(cm.Blues)
            self.set_cmaplev(np.arange(0,0.02+0.002,0.002))
            self.set_cbticks(np.arange(0,0.02+0.002,0.002))
            self.set_cbextmode('max')
            self.set_tit('Specific Humidity Annual Mean')
        elif flag == 'seascyc':
            self.set_varname('vapor.seascyc')
            self.set_cmap(cm.RdBu_r)
            self.set_cmaplev(np.arange(-0.01,0.01+0.001,0.001))
            self.set_cbticks(np.arange(-0.01,0.01+0.002,0.002))
            self.set_cbextmode('both')
            self.set_tit('Specific Humidity Seasonal Cycle')
        else:
            self.set_varname('vapor')
            self.set_cmap(cm.Blues)
            self.set_cmaplev(12)
            self.set_cbextmode('both')
            self.set_tit('Specific Humidity')
        return self

    def ice(self):
        flag = self.get_flag()
        self.set_units(' ')
        if self.get_flag() == 'amean':
            self.set_varname('ice.amean')
            self.set_cmap(cm.Blues_r)
            self.set_cmaplev(np.arange(0,1+0.05,0.05))
            self.set_cbticks(np.arange(0,1+0.1,0.1))
            self.set_cbextmode('both')
            self.set_tit('Ice Annual Mean')
        elif flag == 'seascyc':
            self.set_varname('ice.seascyc')
            self.set_cmap(cm.RdBu_r)
            self.set_cmaplev(np.arange(0,1+0.05,0.05))
            self.set_cbticks(np.arange(0,1+0.1,0.1))
            self.set_cbextmode('both')
            self.set_tit('Ice Seasonal Cycle')
        else:
            self.set_varname('ice')
            self.set_cmap(cm.Blues_r)
            self.set_cmaplev(12)
            self.set_cbextmode('both')
            self.set_tit('Ice')
        return self

    def assign_var(self):
        name = self.get_defname()
        if name in self.defvar:
            return eval('self.{}()'.format(name))
        else:
            return self

class plot_difference(plot_param):
    txt = 'Anomaly'
    def tatmos(self):
        flag = self.get_flag()
        self.set_units('[K]')
        self.set_cbextmode('both')
        self.set_cmap(cm.RdBu_r)
        if self.get_flag() == 'amean':
            self.set_varname('tatmos.amean')
            self.set_tit('Atmospheric Temperature Annual Mean '+self.txt)
            self.set_cmaplev(np.arange(-8,8+1,1))
            self.set_cbticks(np.arange(-8,8+1,1))
        elif self.get_flag() == 'seascyc':
            self.set_varname('tatmos.seascyc')
            self.set_tit('Atmospheric Temperature Seasonal Cycle '+self.txt)
            self.set_cmaplev(np.arange(-4,4+0.5,0.5))
            self.set_cbticks(np.arange(-4,4+1,1))
        else:
            self.set_varname('tatmos')
            self.set_cmaplev(12)
            self.set_tit('Atmospheric Temperature '+self.txt)
        return self

    def tsurf(self):
        flag = self.get_flag()
        self.set_units('[K]')
        self.set_cbextmode('both')
        self.set_cmap(cm.RdBu_r)
        if flag == 'amean':
            self.set_varname('tsurf.amean')
            self.set_tit('Surface Temperature Annual Mean '+self.txt)
            self.set_cmaplev(np.arange(-8,8+1,1))
            self.set_cbticks(np.arange(-8,8+1,1))
        elif flag == 'seascyc':
            self.set_varname('tsurf.seascyc')
            self.set_tit('Surface Temperature Seasonal Cycle '+self.txt)
            self.set_cmaplev(np.arange(-4,4+0.5,0.5))
            self.set_cbticks(np.arange(-4,4+1,1))
        else:
            self.set_varname('tsurf')
            self.set_cmaplev(12)
            self.set_tit('Surface Temperature '+self.txt)
        return self

    def tocean(self):
        flag = self.get_flag()
        self.set_units('[K]')
        self.set_cbextmode('both')
        self.set_cmap(cm.RdBu_r)
        if self.get_flag() == 'amean':
            self.set_varname('tocean.amean')
            self.set_cmaplev(np.arange(-4,4+0.5,0.5))
            self.set_cbticks(np.arange(-4,4+1,1))
            self.set_tit('Ocean Temperature Annual Mean '+self.txt)
        elif flag == 'seascyc':
            self.set_varname('tocean.seascyc')
            self.set_cmaplev(np.arange(-1,1+0.1,0.1))
            self.set_cbticks(np.arange(-1,1+0.2,0.2))
            self.set_tit('Ocean Temperature Seasonal Cycle '+self.txt)
        else:
            self.set_varname('tocean')
            self.set_cmaplev(12)
            self.set_tit('Ocean Temperature '+self.txt)
        return self

    def precip(self):
        flag = self.get_flag()
        self.set_units('[mm][day-1]')
        self.set_cbextmode('both')
        self.set_cmap(cm.RdBu_r)
        if self.get_flag() == 'amean':
            self.set_varname('precip.amean')
            self.set_tit('Precipitation Annual Mean '+self.txt)
            self.set_cmaplev(np.arange(-2,2+0.2,0.2))
            self.set_cbticks(np.arange(-2,2+0.4,0.4))
        elif flag == 'seascyc':
            self.set_varname('precip.seascyc')
            self.set_tit('Precipitation Seasonal Cycle '+self.txt)
            self.set_cmaplev(np.arange(-2,2+0.2,0.2))
            self.set_cbticks(np.arange(-2,2+0.4,0.4))
        else:
            self.set_varname('precip')
            self.set_cmaplev(12)
            self.set_tit('Precipitation '+self.txt)
        return self

    def eva(self):
        flag = self.get_flag()
        self.set_units('[mm][day-1]')
        self.set_cbextmode('both')
        self.set_cmap(cm.RdBu_r)
        if self.get_flag() == 'amean':
            self.set_varname('eva.amean')
            self.set_tit('Evaporation Annual Mean '+self.txt)
            self.set_cmaplev(np.arange(-2,2+0.2,0.2))
            self.set_cbticks(np.arange(-2,2+0.4,0.4))
        elif flag == 'seascyc':
            self.set_varname('eva.seascyc')
            self.set_tit('Evaporation Seasonal Cycle '+self.txt)
            self.set_cmaplev(np.arange(-2,2+0.2,0.2))
            self.set_cbticks(np.arange(-2,2+0.4,0.4))
        else:
            self.set_varname('eva')
            self.set_cmaplev(12)
            self.set_tit('Evaporation '+self.txt)
        return self

    def qcrcl(self):
        flag = self.get_flag()
        self.set_units('[mm][day-1]')
        self.set_cbextmode('both')
        self.set_cmap(cm.RdBu_r)
        if self.get_flag() == 'amean':
            self.set_varname('qcrcl.amean')
            self.set_tit('Circulation Annual Mean '+self.txt)
            self.set_cmaplev(np.arange(-2,2+0.2,0.2))
            self.set_cbticks(np.arange(-2,2+0.4,0.4))
        elif flag == 'seascyc':
            self.set_varname('qcrcl.seascyc')
            self.set_tit('Circulation Seasonal Cycle '+self.txt)
            self.set_cmaplev(np.arange(-2,2+0.2,0.2))
            self.set_cbticks(np.arange(-2,2+0.4,0.4))
        else:
            self.set_varname('qcrcl')
            self.set_cmaplev(12)
            self.set_tit('Circulation '+self.txt)
        return self

    def vapor(self):
        flag = self.get_flag()
        self.set_units(' ') # ADD UNITS!
        self.set_cbextmode('both')
        self.set_cmap(cm.RdBu_r)
        if self.get_flag() == 'amean':
            self.set_varname('vapor.amean')
            self.set_tit('Specific Humidity Annual Mean '+self.txt)
            self.set_cmaplev(np.arange(-5e-3,5e-3+5e-4,5e-4))
            self.set_cbticks(np.arange(-5e-3,5e-3+1e-3,1e-3))
        elif flag == 'seascyc':
            self.set_varname('vapor.seascyc')
            self.set_tit('Specific Humidity Seasonal Cycle '+self.txt)
            self.set_cmaplev(np.arange(-5e-3,5e-3+5e-4,5e-4))
            self.set_cbticks(np.arange(-5e-3,5e-3+1e-3,1e-3))
        else:
            self.set_varname('vapor')
            self.set_cmaplev(12)
            self.set_tit('Specific Humidity '+self.txt)
        return self

    def ice(self):
        flag = self.get_flag()
        self.set_units(' ')
        self.set_cbextmode('both')
        self.set_cmap(cm.RdBu_r)
        if self.get_flag() == 'amean':
            self.set_varname('ice.amean')
            self.set_tit('Ice Annual Mean '+self.txt)
            self.set_cmaplev(np.arange(-1,1+0.1,0.1))
            self.set_cbticks(np.arange(-1,1+0.2,0.2))
        elif flag == 'seascyc':
            self.set_varname('ice.seascyc')
            self.set_tit('Ice Seasonal Cycle '+self.txt)
            self.set_cmaplev(np.arange(-1,1+0.1,0.1))
            self.set_cbticks(np.arange(-1,1+0.2,0.2))
        else:
            self.set_varname('ice '+self.txt)
            self.set_cmaplev(12)
            self.set_tit('Ice')
        return self

    def assign_var(self):
        name = self.get_defname()
        if name in self.defvar:
            return eval('self.{}()'.format(name))
        else:
            return self
