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
from datetime import datetime as dtime

class constants:
    def __init__(self):
        pass

    @staticmethod
    def t():
        return np.arange(17522904.,17531652.+12,12)
    @staticmethod
    def lat():
        return np.arange(-88.125,88.125+3.75,3.75)
    @staticmethod
    def lon():
        return np.arange(0,360,3.75)
    @staticmethod
    def dx():
        return len(constants.lon())
    @staticmethod
    def dy():
        return len(constants.lat())
    @staticmethod
    def dt():
        return len(constants.t())
    @staticmethod
    def cloud_file():
        return r'/Users/dmar0022/university/phd/greb-official/input/isccp.cloud_cover.clim'
    @staticmethod
    def control_def_file():
        return r'/Users/dmar0022/university/phd/greb-official/output/control.default'
    @staticmethod
    def shape_for_bin():
    # 'Shape must be in the form (tdef,ydef,xdef)'
        return (constants.dt(),constants.dy(),constants.dx())
    @staticmethod
    def to_shape_for_bin(data):
        def_sh = constants.shape_for_bin()
        sh=data.shape
        if len(sh) != 3: raise Exception('data must be 3D, in the form {}x{}x{}'.format(def_sh[0],def_sh[1],def_sh[2]))
        if len(set(sh)) != 3: raise Exception('data shape must be in the form {}x{}x{}'.format(def_sh[0],def_sh[1],def_sh[2]))
        if ((sh[0] not in def_sh) or (sh[1] not in def_sh) or (sh[2] not in def_sh)):
            raise Exception('data shape must be in the form {}x{}x{}'.format(def_sh[0],def_sh[1],def_sh[2]))
        if sh != def_sh:
            indt=sh.index(def_sh[0])
            indy=sh.index(def_sh[1])
            indx=sh.index(def_sh[2])
            data = data.transpose(indt,indy,indx)
        return data

def create_clouds(time = None, longitude = None, latitude = None, value = 1,
                  cloud_base = None, outpath = None):
    '''
    - Create clouds from scratch, or by modifying an existent cloud matrix ("cloud_base").
    - Every coordinate can be specified in the form:
    - coord_name = [coord_min, coord_max] --> To apply changes only to that portion of that coordinate;
    - If coord_name = 'time', default format is '%m-%d' (The year is automatically set at 2000)
      (e.g. '03-04' for 4th March).
      To specify your own formatn (for month and day) use the form: [time_min,time_max,format];
    - If coord_name = 'latitude', the format is [lat_min,lat_max] in N-S degrees (-90 ÷ 90)
      (e.g. [-20,40] is from 20S to 40N);
    - If coord_name = 'longitude', the format is [lon_min,lon_max] in E-W degrees (-180 ÷ 180)
      (e.g. [-10,70] is from 10E to 70W);
    - "value" can be an integer, float or function to be applied element-wise to the "cloud_base"
      (e.g. "lambda x: x*1.1").
    '''
    def check_lon(min,max):
        if (min*max) > 0:
            return (min<max)
        else:
            return (min>max)
    def switch_lon(x):
        if isinstance(x,list):
            if len(x) == 1:
                return 360+x if x<0 else x
            else:
                return [360+k if k<0 else k for k in x]
        else:
            return 360+x if x<0 else x
    def to_grebtime(date_str,fmt = '%y-%m-%d'):
        return dtime.strptime(date_str,fmt).toordinal()*24+24
    # Define constants
    def_t=constants.t()
    def_lat=constants.lat()
    def_lon=constants.lon()
    dt = constants.dt()
    dx = constants.dx()
    dy = constants.dy()
    # Check coordinates and constrain them
    # TIME
    if time is not None:
        t_exc = '"time" must be an int or date_string in the form [time_min,time_max]\n'+\
              'The date_string must have the format "%m-%d" (e.g. "03-04" for 4th March).\n'+\
              'To specify your own format use the form: [time_min,time_max,format]'
        fmt = '%y-%m-%d'
        if not isinstance(time,list):
            if (isinstance(time,float) or isinstance(time,int) or isinstance(time,str)):
                time = [time]
            else:
                raise Exception(t_exc)
        if len(time) == 1:
            if isinstance(time[0],str):
                t_min = t_max = to_grebtime('00-'+time[0])
            else:
                t_min = t_max = int(time[0])
        elif len(time) == 2:
            if isinstance(time[0],str):
                t_min = to_grebtime('00-'+time[0])
                t_max = to_grebtime('00-'+time[1])
            else:
                t_min = int(time[0])
                t_max = int(time[1])
        elif len(time) == 3:
            if isinstance(time[0],str):
                t_min = to_grebtime('00-'+time[0],'%y-'+time[2])
                t_max = to_grebtime('00-'+time[1],'%y-'+time[2])
            else:
                raise Exception(t_exc)
        else:
            raise Exception(t_exc)
        ind_t=np.where((def_t>=t_min) & (def_t<=t_max))[0]
    else:
        ind_t=np.where((def_t>=def_t.min()) & (def_t<=def_t.max()))[0]
    # LONGITUDE
    if longitude is not None:
        lon_exc = '"longitude" must be a number or in the form [lon_min,lon_max]'
        if (isinstance(longitude,float) or isinstance(longitude,int)):
            longitude = [longitude]
        if isinstance(longitude,list):
            if len(longitude) > 2:
                raise Exception(lon_exc)
            else:
                if np.any(list(map(lambda l: (l > 180 or l < -180),longitude))):
                        raise Exception('"longitude" must be in the range [-180÷180]')
                lon_min,lon_max = switch_lon(longitude)
        else:
            raise Exception(lon_exc)
        if check_lon(lon_min,lon_max):
            ind_lon=np.where((def_lon>=lon_min) & (def_lon<=lon_max))[0]
        else:
            ind_lon=np.where((def_lon>=lon_min) | (def_lon<=lon_max))[0]
    else:
        ind_lon=np.where((def_lon>=def_lon.min()) & (def_lon<=def_lon.max()))[0]
    # LATITUDE
    if latitude is not None:
        lat_exc = '"latitude" must be a number or in the form [lat_min,lat_max]'
        if (isinstance(latitude,float) or isinstance(latitude,int)):
            latitude = [latitude]
        if isinstance(latitude,list):
            if len(latitude) > 2:
                raise Exception(lat_exc)
            else:
                if np.any(list(map(lambda l: (l > 90 or l < -90),latitude))):
                        raise Exception('"latitude" must be in the range [-90÷90]')
                lat_min,lat_max = latitude
        else:
            raise Exception(lat_exc)
        if lat_min < lat_max:
            ind_lat=np.where((def_lat>=lat_min) & (def_lat<=lat_max))[0]
        else:
            ind_lat=np.where((def_lat>=lat_min) | (def_lat<=lat_max))[0]
    else:
        ind_lat=np.where((def_lat>=def_lat.min()) & (def_lat<=def_lat.max()))[0]
    if cloud_base is not None:
        if isinstance(cloud_base,str):
            data=data_from_binary(cloud_base)['cloud']
        elif isinstance(cloud_base,np.ndarray):
            data = cloud_base
        else:
            raise Exception('"cloud_base" must be a valid .ctl or .bin file or a numpy.ndarray matrix of the cloud data')
        data = constants.to_shape_for_bin(data)
    else:
        data = np.zeros((dt,dy,dx))
    # Change values
    if (isinstance(value,float) or isinstance(value,int)):
        data[ind_t[:,None,None],ind_lat[:,None],ind_lon] = value
    elif callable(value):
        data[ind_t[:,None,None],ind_lat[:,None],ind_lon] = value(data[ind_t[:,None,None],ind_lat[:,None],ind_lon])
    else:
        raise Exception('"value" must be a number or function to apply to the "cloud_base" (e.g. "lambda x: x*1.1")')
    # Correct value above 1 or below 0
    data=np.where(data<=1,data,1)
    data=np.where(data>=0,data,0)
    # Write .bin and .ctl files
    vars = {'cloud':data}
    if outpath is None:
        outpath='/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.ctl'
    create_bin_ctl(outpath,vars)

def get_art_cloud_filename(filename):
    txt='exp-930.geoeng.'
    if txt in filename:
        art_cloud_name = filename[filename.index(txt)+len(txt):]
        return os.path.join('/Users/dmar0022/university/phd/greb-official/artificial_clouds',
                           art_cloud_name)
    else:
       return None

def input_(def_input,argv=1):
    if (argv < 1 or not isinstance(argv,int)): raise Exception('argv must be an integer greater than 0')
    try:
        input=sys.argv[argv]
        if ((argv == 1 and input == '-f') or (argv==2 and os.path.splitext(input)[1]=='.json')):
            return rmext(def_input) if isinstance(def_input,str) else def_input
        else:
            return rmext(input) if isinstance(input,str) else input
    except(IndexError): return rmext(def_input) if isinstance(def_input,str) else def_input

def plot_clouds(filename,outpath=None):
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
# Plot annual data
    am= plot_param.from_cube(annual_mean(data), cmap=cm.Greys_r, varname = name+'.amean',
                             cmaplev = np.arange(0,1+0.05,0.05),units = '',
                             cbticks = np.arange(0,1+0.1,0.1),
                             cbextmode = 'neither', tit = name + ' Annual Mean')
    plt.figure()
    am.plot(outpath = outpath, coast_param = {'edgecolor':[0,.5,0.3]},statistics=True)
# Plot seasonal cycle data
    am= plot_param.from_cube(seasonal_cycle(data), varname = name+'.seascyc',
                             cmaplev = np.arange(-1,1+0.1,0.1),units = '',
                             cbticks = np.arange(-1,1+0.2,0.2),
                             tit = name + ' Seasonal Cycle')
    plt.figure()
    am.plot(outpath = outpath, coast_param = {'edgecolor':[0,.5,0.3]},statistics=True)
    os.remove(filename+'.nc')

def ignore_warnings():
# Ignore warnings
    if not sys.warnoptions:
        warnings.simplefilter("ignore")

def data_from_binary(filename,flag='raw'):
    # 1st version, quicker but not precise on time corrections
    '''
    The flag can be:
    "raw" --> no corrections are performed on the data
    "correct_units" --> units correction is performed for some variables ("precip","eva" and "qcrcl")
    "correct_time" --> time correction is performed so that data belonging to the same MONTH will be averaged
    "correct_all" (default) --> correct both time values and units
    '''
    # If flag is not "raw" use data_from_binary_2 (more precise)
    def data_from_binary_2(filename,flag='correct_all'):
    # 2nd version, slower but precise on time corrections
        filename = rmext(filename)
        bin2netCDF(filename)
        data = iris.load(filename+'.nc')
        if flag in ['correct_units','correct_all']:
            data = parsevar(data)
        keys = [d.var_name for d in data]
        if flag in ['correct_time','correct_all']:
            for d in data: iris.coord_categorisation.add_month(d, 'time', name='month')
            data = [d.aggregated_by('month',iris.analysis.MEAN) for d in data]
        vals = [d.data.data.squeeze() for d in data]
        dic = dict(zip(keys,vals))
        return dic

    if flag != 'raw':
        return data_from_binary_2(filename,flag)
    filename = rmext(filename)
    with open(filename+'.ctl','r') as f:
        b=f.read().split('\n')
    ind = np.where(list(map(lambda x: 'vars' in x.split(),b)))[0][0]
    vars=int(b[ind].split()[1])
    dt = int(b[np.where(list(map(lambda x: 'tdef' in x.split(),b)))[0][0]].split()[1])
    dx = int(b[np.where(list(map(lambda x: 'xdef' in x.split(),b)))[0][0]].split()[1])
    dy = int(b[np.where(list(map(lambda x: 'ydef' in x.split(),b)))[0][0]].split()[1])
    keys = []
    for i in np.arange(vars):
        keys.append(b[ind+1+i].split()[0])
    with open(filename+'.bin','rb') as f:
        v = np.fromfile(f,dtype=np.float32).reshape(dt,vars,dy,dx).transpose(1,0,2,3)
        vals=[v[i,...] for i in np.arange(vars)]
    dic = dict(zip(keys,vals))
    return dic

def rmext(filename):
    path,ext = os.path.splitext(filename)
    if ext not in ['.ctl','.bin','.']: path = path+ext
    return path

def create_bin(path,vars):
    path = rmext(path)
    with open(path+'.bin','wb') as f:
        for v in vars: f.write(v)

def create_ctl(path, varnames = ['clouds'], xdef = constants.dx(),
               ydef = constants.dy(), zdef = 1, tdef = constants.dt()):
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
    varvals = [constants.to_shape_for_bin(v) for v in varvals]
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

def anomalies(cubes,cubes_base):
    fl=False
    if not isinstance(cubes,list):
        cubes = [cubes]
        fl=True
    if not isinstance(cubes_base,list): cubes_base = [cubes_base]
    # get var names
    varnames=[var.var_name for var in cubes]
    varnames_base=[var.var_name for var in cubes_base]
    # compute anomalies between same variables
    diff = []
    for i,var in enumerate(varnames):
        if var in varnames_base:
            ind = varnames_base.index(var)
            d = cubes[i]-cubes_base[ind]
            d.var_name = cubes[i].var_name
            diff.append(d)
    return diff[0] if fl else diff

def variation(cubes,cubes_base,func='weighted'):
    ''' The possibilities for FUNC are the following:
        "basic" --> Basic rate of change: (x - x_ref)/|x_ref|
        "weighted" --> ((x - x_ref)/((|x|-|x_ref|)/2))*max(x,x_ref)
        user defined function --> an example could be: lambda x,x-ref: x-x_ref
    '''
    fl=False
    if not isinstance(cubes,list):
        cubes = [cubes]
        fl=True
    if not isinstance(cubes_base,list): cubes_base = [cubes_base]
    # get var names
    varnames=[var.var_name for var in cubes]
    varnames_variation=[var.var_name for var in cubes_base]
    # compute variations between same variables
    variat = []
    c=cubes
    b=cubes_base
    _abs=iris.analysis.maths.abs
    _max=iris.analysis.maths.apply_ufunc
    for i,var in enumerate(varnames):
        if (var in varnames_variation):
            k= varnames_variation.index(var)
            if func == 'basic':
                v = ((c[i]-b[k])/_abs(b[k]))*100
            elif func == 'weighted':
                v = 2*((c[i]-b[k])/(_abs(c[i])+_abs(b[k])))*_max(np.maximum,c[i],b[k])*100
            else:
                v = func(c[i],b[k])*100
            v.var_name = cubes[i].var_name
            variat.append(v)
    return variat[0] if fl else variat

def parsevar(cubes):
    # Initialize output variables
    fl=False
    if not isinstance(cubes,list):
        cubes = [cubes]
        fl=True
    varnames=[var.var_name for var in cubes]
    for var in cubes:
        var.long_name = None
        defvar = ['tatmos','tsurf','tocean','precip','eva','qcrcl','vapor','ice']
    # TATMOS
    id = 'tatmos'
    if id in varnames:
        ind = varnames.index(id)
        cubes[ind].units=''
    # TSURF
    id = 'tsurf'
    if id in varnames:
        ind = varnames.index(id)
        cubes[ind].units=''
    # TOCEAN
    id = 'tocean'
    if id in varnames:
        ind = varnames.index(id)
        cubes[ind].units=''
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
    # VAPOR
    id = 'vapor'
    if id in varnames:
        ind = varnames.index(id)
        cubes[ind].units=''
    # ICE
    id = 'ice'
    if id in varnames:
        ind = varnames.index(id)
        cubes[ind].units=''
    return cubes[0] if fl else cubes

class plot_param:
    ext = 'png'
    defvar = ['tatmos','tsurf','tocean','precip','eva','qcrcl','vapor','ice','cloud']
    defflags = ['amean','seascyc','anom','variat']

    def __init__(self, cube = None, units = None, cmap = None, cmaplev = None,
                 cbticks = None, cbextmode = None, defname = None,
                 varname = None, tit = None, flags = None):

        self.cube = cube
        self.cmap = cmap
        self.cmaplev = cmaplev
        self.cbticks = cbticks
        self.cbextmode = cbextmode
        self.units = units
        self.defname = defname
        self.varname = varname
        self.tit = tit
        self.flags = flags if (flags is None or isinstance(flags,list)) else [flags]

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

    def set_flags(self,flags):
        if not isinstance(flags,list): flags=[flags]
        for f in flags:
            if f not in self.defflags: raise Exception('{} is not a recognized flag'.format(f))
        self.flags = list(set(flags))

    def add_flags(self,flags):
        if not isinstance(flags,list): flags=[flags]
        oldflags=self.get_flags()
        if oldflags:
            self.set_flags(list(set(oldflags+flags)))
        else:
            self.set_flags(list(set(flags)))

    def get_cube(self):
        return self.cube

    def get_data(self):
        return self.get_cube().data

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

    def get_flags(self):
        return self.flags

    def plot(self, outpath = None, ax = None, projection = ccrs.Robinson(),
             coast_param = {},
             land_param = {'edgecolor':'face', 'facecolor':'black'},
             title_param = {'fontsize':12},
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
            txt = ('gmean = {:.3f}'+'\n'+\
                  'std = {:.3f}'+'\n'+\
                  'rms = {:.3f}').format(self.gmean(),self.std(),self.rms())
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
    def get_defflags(cls):
        return cls.defflags

    @classmethod
    def set_ext(cls,ext):
        cls.ext = ext

    @classmethod
    def set_defvar(cls,vars):
        if not isinstance(vars,list): vars = [vars]
        cls.defvar = vars

    @classmethod
    def add_defvar(cls,vars):
        if not isinstance(vars,list): vars = [vars]
        cls.set_defvar(list(set(cls.get_defvar()+vars)))

    @classmethod
    def set_defflags(cls,flags):
        if not isinstance(flags,list): flags = [flags]
        cls.defflags = flags

    @classmethod
    def add_defflags(cls,flags):
        if not isinstance(flags,list): flags = [flags]
        cls.set_defflags(list(set(cls.get_defflags()+flags)))

    @classmethod
    def from_cube(cls, cube, units = None, cmap = cm.RdBu_r, cmaplev = None,
                  cbticks = None, cbextmode = 'both', varname = None,
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
        self.add_flags('amean')
        return self

    def to_seasonal_cycle(self):
        tit = self.get_tit()
        cube = self.get_cube()
        newcube = seasonal_cycle(cube)
        self.set_cube(newcube)
        self.set_varname(newcube.var_name)
        if tit is None:
            self.set_tit(self.get_varname()+'.seascyc')
        self.add_flags('seascyc')
        return self

    def to_anomalies(self,cube_base):
        fl = self.get_flags()
        varname = self.get_varname()
        cube = self.get_cube()
        if 'amean' in fl:
            cube_base = annual_mean(cube_base)
        elif 'seascyc' in fl:
            cube_base = seasonal_cycle(cube_base)
        newcube = anomalies(cube,cube_base)
        self.set_cube(newcube)
        self.set_varname(varname)
        self.add_flags('anom')
        return self

    def to_variation(self,cube_base,func='weighted'):
        fl = self.get_flags()
        varname = self.get_varname()
        cube = self.get_cube()
        if 'amean' in fl:
            cube_base = annual_mean(cube_base)
        elif 'seascyc' in fl:
            cube_base = seasonal_cycle(cube_base)
        newcube = variation(cube,cube_base,func)
        self.set_cube(newcube)
        self.set_varname(varname)
        self.add_flags('variat')
        return self

    def gmean(self):
        return self.get_cube().data.mean()

    def std(self):
        return self.get_cube().data.std()

    def rms(self):
        return np.sqrt((self.get_cube().data**2).mean())
# ====================================================================
# ====================================================================
# ====================================================================
    def tatmos(self):
        flags = self.get_flags()
        self.set_varname('tatmos')
        self.set_units('[K]')
        self.set_tit('Atmospheric Temperature')
        self.set_cmap(cm.RdBu_r)
        if 'anom' in flags:
            if 'amean' in flags:
                self.set_cmaplev(np.arange(-8,8+1,1))
                self.set_cbticks(np.arange(-8,8+1,1))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-4,4+0.5,0.5))
                self.set_cbticks(np.arange(-4,4+1,1))
        else:
            if 'amean' in flags:
                self.set_cmaplev(np.arange(223,323+5,5))
                self.set_cbticks(np.arange(223,323+10,10))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-20,20+2,2))
                self.set_cbticks(np.arange(-20,20+4,4))
        return self

    def tsurf(self):
        flags = self.get_flags()
        self.set_varname('tsurf')
        self.set_units('[K]')
        self.set_tit('Surface Temperature')
        self.set_cmap(cm.RdBu_r)
        if 'anom' in flags:
            if 'amean' in flags:
                self.set_cmaplev(np.arange(-4,4+0.5,0.5))
                self.set_cbticks(np.arange(-4,4+1,1))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-4,4+0.5,0.5))
                self.set_cbticks(np.arange(-4,4+1,1))
        else:
            if 'amean' in flags:
                self.set_cmaplev(np.arange(223,323+5,5))
                self.set_cbticks(np.arange(223,323+10,10))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-20,20+2,2))
                self.set_cbticks(np.arange(-20,20+4,4))
        return self

    def tocean(self):
        flags = self.get_flags()
        self.set_varname('tocean')
        self.set_units('[K]')
        self.set_tit('Ocean Temperature')
        self.set_cmap(cm.RdBu_r)
        if 'anom' in flags:
            if 'amean' in flags:
                self.set_cmaplev(np.arange(-4,4+0.5,0.5))
                self.set_cbticks(np.arange(-4,4+1,1))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                self.set_cbticks(np.arange(-1,1+0.2,0.2))
        else:
            if 'amean' in flags:
                self.set_cmaplev(np.arange(273,303+5,3))
                self.set_cbticks(np.arange(273,303+10,3))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-1,1+1e-1,1e-1))
                self.set_cbticks(np.arange(-1,1+2e-1,2e-1))
        return self

    def precip(self):
        flags = self.get_flags()
        self.set_varname('precip')
        self.set_units('[mm][day-1]')
        self.set_tit('Precipitation')
        self.set_cmap(cm.GnBu)
        if 'anom' in flags:
            if 'amean' in flags:
                self.set_cmaplev(np.arange(-2,2+0.2,0.2))
                self.set_cbticks(np.arange(-2,2+0.4,0.4))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-2,2+0.2,0.2))
                self.set_cbticks(np.arange(-2,2+0.4,0.4))
        else:
            if 'amean' in flags:
                self.set_cmaplev(np.arange(0,9+1,1))
                self.set_cbticks(np.arange(0,9+1,1))
                self.set_cbextmode('max')
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-6,6+1,1))
                self.set_cmaplev(np.arange(-6,6+1,1))
        return self

    def eva(self):
        flags = self.get_flags()
        self.set_units('[mm][day-1]')
        self.set_varname('eva')
        self.set_tit('Evaporation')
        self.set_cmap(cm.GnBu)
        if 'anom' in flags:
            if 'amean' in flags:
                self.set_cmaplev(np.arange(-2,2+0.2,0.2))
                self.set_cbticks(np.arange(-2,2+0.4,0.4))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-2,2+0.2,0.2))
                self.set_cbticks(np.arange(-2,2+0.4,0.4))
        else:
            if 'amean' in flags:
                self.set_cmap(cm.Blues)
                self.set_cmaplev(np.arange(0,10+1,1))
                self.set_cbticks(np.arange(0,10+1,1))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-3,3+0.5,0.5))
                self.set_cbticks(np.arange(-3,3+0.5,0.5))
        return self

    def qcrcl(self):
        flags = self.get_flags()
        self.set_units('[mm][day-1]')
        self.set_varname('qcrcl')
        self.set_tit('Circulation')
        self.set_cmap(cm.RdBu_r)
        if 'anom' in flags:
            if 'amean' in flags:
                self.set_cmaplev(np.arange(-2,2+0.2,0.2))
                self.set_cbticks(np.arange(-2,2+0.4,0.4))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-2,2+0.2,0.2))
                self.set_cbticks(np.arange(-2,2+0.4,0.4))
        else:
            if 'amean' in flags:
                self.set_cmaplev(np.arange(-8,8+1))
                self.set_cbticks(np.arange(-8,8+2,2))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-6,6+1,1))
                self.set_cmaplev(np.arange(-6,6+1,1))
        return self

    def vapor(self):
        flags = self.get_flags()
        self.set_units(' ') # ADD UNITS!
        self.set_varname('vapor')
        self.set_tit('Specific Humidity')
        self.set_cmap(cm.RdBu_r)
        if 'anom' in flags:
            if 'amean' in flags:
                self.set_cmaplev(np.arange(-5e-3,5e-3+5e-4,5e-4))
                self.set_cbticks(np.arange(-5e-3,5e-3+1e-3,1e-3))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-5e-3,5e-3+5e-4,5e-4))
                self.set_cbticks(np.arange(-5e-3,5e-3+1e-3,1e-3))
        else:
            if 'amean' in flags:
                self.set_cmap(cm.Blues)
                self.set_cmaplev(np.arange(0,0.02+0.002,0.002))
                self.set_cbticks(np.arange(0,0.02+0.002,0.002))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-0.01,0.01+0.001,0.001))
                self.set_cbticks(np.arange(-0.01,0.01+0.002,0.002))
        return self

    def ice(self):
        flags = self.get_flags()
        self.set_units(' ')
        self.set_varname('ice')
        self.set_tit('Ice')
        self.set_cmap(cm.Blues_r)
        if 'anom' in flags:
            if 'amean' in flags:
                self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                self.set_cbticks(np.arange(-1,1+0.2,0.2))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                self.set_cbticks(np.arange(-1,1+0.2,0.2))
        else:
            if 'amean' in flags:
                self.set_cmaplev(np.arange(0,1+0.05,0.05))
                self.set_cbticks(np.arange(0,1+0.1,0.1))
                self.set_cbextmode('max')
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(0,1+0.05,0.05))
                self.set_cbticks(np.arange(0,1+0.1,0.1))
        return self

        def cloud(self):
            flags = self.get_flags()
            self.set_units(' ')
            self.set_varname('cloud')
            self.set_tit('Clouds')
            self.set_cmap(cm.Greys_r)
            if 'anom' in flags:
                if 'amean' in flags:
                    self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                    self.set_cbticks(np.arange(-1,1+0.2,0.2))
                elif 'seascyc' in flags:
                    self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                    self.set_cbticks(np.arange(-1,1+0.2,0.2))
            else:
                if 'amean' in flags:
                    self.set_cmaplev(np.arange(0,1+0.05,0.05))
                    self.set_cbticks(np.arange(0,1+0.1,0.1))
                    self.set_cbextmode('neither')
                elif 'seascyc' in flags:
                    self.set_cmaplev(np.arange(0,1+0.05,0.05))
                    self.set_cbticks(np.arange(0,1+0.1,0.1))
            return self

    def assign_var(self):
        name = self.get_defname()
        if name in self.defvar:
            return eval('self.{}().set_param()'.format(name))
        else:
            return self

    def set_param(self):
        flags = self.get_flags()
        if 'amean' in flags:
            txt='amean'
            tit = 'Annual Mean'
        elif 'seascyc' in flags:
            txt='seascyc'
            tit = 'Seasonal Cycle'
            self.set_cmap(cm.RdBu_r)
            self.set_cbextmode('both')
        else:
            txt=''
            tit = ''
            self.set_cmaplev(12)

        if 'variat' in flags:
            tit2='Change Rate'
            self.set_units('%')
            self.set_cmap(cm.PuOr_r)
            self.set_cmaplev(np.arange(-100,100+10,10))
            self.set_cbticks(np.arange(-100,100+20,20))
            self.set_cbextmode('both')
        elif 'anom' in flags:
            tit2= 'Anomaly'
            self.set_cmap(cm.RdBu_r)
            self.set_cbextmode('both')
        else:
            tit2= ''

        self.set_varname('.'.join([self.get_varname(),txt]))
        self.set_tit(' '.join([self.get_tit(),tit,tit2]))
        return self
