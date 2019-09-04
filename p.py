# Libraries
import sys
import warnings
import os
import numpy as np
import iris
from cdo import Cdo
import iris.coord_categorisation
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import iris.quickplot as qplt
import iris.plot as iplt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime as dtime
import matplotlib.dates as mdates
from scipy import interpolate
import matplotlib.gridspec as gridspec


def cube_from_data(data, var_name = None, units = None, time = None, latitude=None, longitude=None):
    from cf_units import Unit
    if time is not None:
        tunits=Unit('hours since 1-1-1 00:00:00', calendar='gregorian')
        time = iris.coords.DimCoord(time,standard_name='time',units=tunits)
    if latitude is not None:
        latitude = iris.coords.DimCoord(latitude,standard_name='latitude',units='degrees')
    if longitude is not None:
        longitude = iris.coords.DimCoord(longitude,standard_name='longitude',units='degrees'
                                                               ,circular = True)
    coords=list(filter(None,[time,latitude,longitude]))
    coords_and_dims = list(zip(coords,np.arange(len(coords))))
    def_cube = iris.cube.Cube(data, var_name=var_name, units = units,
        dim_coords_and_dims = coords_and_dims)
    return def_cube

def plot_clouds_and_tsurf(*cloudfiles, years=50, coords = None, labels = None):
    import matplotlib.ticker as ticker
    def get_tsurf(*fnames):
        mdays=np.array([31,28,31,30,31,30,31,31,30,31,30,31])
        tsurf = []
        for f in fnames:
            t=data_from_binary(f,'monthly')['tsurf']
            t=np.repeat(t,mdays*2,axis=0)
            s=t.shape
            t_=np.zeros(s)
            for i in np.arange(s[1]):
                for j in np.arange(s[2]):
                    t_[:,i,j]=spline_interp(t[:,i,j])
            tsurf.append(t_)
        return tsurf

    cloud = [data_from_binary(f)['cloud'] for f in cloudfiles]
    cloud_ctr = data_from_binary(constants.cloud_def_file())['cloud']
    tfiles = [get_scenario_filename(f,years=years) for f in cloudfiles]
    tsurf = get_tsurf(*tfiles)
    tsurf_ctr = get_tsurf(constants.control_def_file())

    cloud_anomaly = [c-cloud_ctr for c in cloud]
    tsurf_anomaly = [(t-tsurf_ctr).squeeze() for t in tsurf]
    if coords is None:
        coords = [(42,12.5),(-37.8,145),(-80,0),(80,0),(0,230)]
    gs = gridspec.GridSpec(2, 2, wspace=0.25, hspace=0.4)

    for coord in coords:
        plt.figure()

        ax1 = plt.subplot(gs[0, 0])
        plot_annual_cycle(coord,*cloud_anomaly)
        ax1.set_ylim([-1,1])
        ax1.set_title('cloud anomaly annual cycle',fontsize=10)
        l=ax1.get_legend()
        if labels is not None:
            for a,label in zip(l.get_texts(),labels): a.set_text(label)
        l.set_bbox_to_anchor([-0.18,1.2])
        for tick in ax1.xaxis.get_major_ticks(): tick.label.set_fontsize(6.5)

        ax2 = plt.subplot(gs[0,1])
        plot_annual_cycle(coord,*tsurf_anomaly)
        ax2.set_ylim([-5,5])
        ax2.set_title('tsurf anomaly annual cycle',fontsize=10)
        ax2.get_legend().remove()
        for tick in ax2.xaxis.get_major_ticks(): tick.label.set_fontsize(6.5)
        ax2.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))

        ax3 = plt.subplot(gs[1, 0])
        plot_annual_cycle(coord,*cloud)
        ax3.set_ylim([0,1])
        ax3.set_title('cloud annual cycle',fontsize=10)
        ax3.get_legend().remove()
        for tick in ax3.xaxis.get_major_ticks(): tick.label.set_fontsize(6.5)

        ax4 = plt.subplot(gs[1,1])
        plot_annual_cycle(coord,*tsurf)
        ax4.set_ylim([223,323])
        ax4.set_title('tsurf annual cycle',fontsize=10)
        ax4.get_legend().remove()
        for tick in ax4.xaxis.get_major_ticks(): tick.label.set_fontsize(6.5)
        ax4.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))

        axP = plt.gcf().axes[1]
        axP.set_position([0.265, 0.95, 0.5, 0.15])


def spline_interp(y):
    mdays=np.array([31,28,31,30,31,30,31,31,30,31,30,31])
    y=y[np.cumsum(mdays*2)-1]
    y=np.insert(y,0,y[0])
    y=np.append(y,y[-1])
    x = (constants.t()/24)[np.cumsum(mdays*2)-1]-15
    x=np.insert(x,0,x[0]-30)
    x=np.append(x,x[-1]+30)
    spl= interpolate.UnivariateSpline(x, y,k=3,s=0)
    x_=constants.t()/24
    y_=spl(x_)
    return y_

def draw_point(lat,lon,ax=None):
    x,y = to_Robinson_cartesian(lat,lon)
    patch = lambda x,y: mpatches.Circle((x,y), radius=6e5, color = 'red',
                                                      transform=ccrs.Robinson())
    ax = plt.axes(projection=ccrs.Robinson()) if ax is None else plt.gca()
    ax.stock_img()
    ax.add_patch(patch(x,y))

def plot_annual_cycle(coord,*data,legend=True, title='Annual Cycle', var = None, draw_point_flag = True):
    from matplotlib.patheffects import Stroke

    i,j=to_greb_indexes(*coord)
    x=constants.t().tolist()
    x=[from_greb_time(a) for a in x]
    for ind,d in enumerate(data):
        try:
            y=d[:,i,j].data
        except:
            y=d[:,i,j]
        plt.plot(x,y,label = '{}'.format(ind+1))
    if legend: plt.legend(loc = 'lower left',bbox_to_anchor=(0,1.001))
    plt.grid()
    plt.title(title,fontsize=15)

    if var == 'cloud':
        plt.ylim([-0.02,1.02])
        m1,m2=plt.xlim()
        plt.hlines(0,m1-100,m2+100,linestyles='--',colors='black',linewidth=0.7)
        plt.hlines(1,m1-100,m2+100,linestyles='--',colors='black',linewidth=0.7)
        plt.xlim([m1,m2])
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    if draw_point_flag:
        # Create an inset GeoAxes showing the location of the Point.
        sub_ax = plt.axes([0.8, 0.9, 0.2, 0.2], projection=ccrs.Robinson())
        sub_ax.outline_patch.set_path_effects([Stroke(linewidth=1.5)])
        draw_point(*coord,sub_ax)

def to_Robinson_cartesian(lat,lon,lon_center = 0):
    from scipy.interpolate import interp1d
    from math import radians
    center = radians(lon_center)
    lon = radians(lon)
    R = 6378137.1
    lat_def = np.arange(0,95,5)
    X_def= [1,0.9986,0.9954,0.9900,0.9822,0.9730,0.9600,0.9427,0.9216,0.8962,
        0.8679,0.8350,0.7986,0.7597,0.7186,0.6732,0.6213,0.5722,0.5322]
    Y_def= [0,0.0620,0.1240,0.1860,0.2480,0.3100,0.3720,0.4340,0.4958,0.5571,
        0.6176,0.6769,0.7346,0.7903,0.8435,0.8936,0.9394,0.9761,1.0000]

    iX = interp1d(lat_def, X_def, kind='cubic')
    iY = interp1d(lat_def, Y_def, kind='cubic')
    x = 0.8487*R*iX(np.abs(lat))*(lon-lon_center)
    y = 1.3523*R*iY(np.abs(lat))
    if (lon % 360) > 180:
        x *= -1;
    if lat < 0:
        y *= -1
    return x,y

def multidim_regression(x,y,x_pred=None,axis=-1,multivariate=False):
    '''
    MULTIDIM_REGRESSION is a function to perform Linear Regression over multi-dimensional arrays.
    It doesn't loop over the dimensions but makes use of np.einsum to perform inner products.
    - Specify the "axis" to set the dimension along which the regression must be computed (default is last dimension).
    - if "multivariate" flag is set to True, multivariate regression is computed;
      the multiple features axis must be the one specified by "axis" + 1.
    '''
    def check_var(x):
        if not isinstance(x,np.ndarray): x = np.array([x])
        if len(x.shape) == 1: x= x.reshape([x.shape[0],1])
        return x

    def check_pred(x):
        if not isinstance(x,np.ndarray): x = np.array([x])
        if len(x.shape) == 1: x = x.reshape([1,x.shape[0]])
        return x

    def check_axis(x,axis,multivariate):
        if axis == -1:
            if multivariate:
                if len(x.shape) > 2:
                    axis = -2
                else:
                    axis = 0
        if multivariate:
            multivariate = axis+1
            if multivariate >= len(x.shape):
                raise Exception('Dimension mismatch')
        else: multivariate = False

        return axis,multivariate

    def check_xy(x,y,axis,multivariate):
        if len(x.shape)!=len(y.shape):
            y = np.expand_dims(y,axis=axis+1)
        dim1 = list(x.shape)
        dim2 = list(y.shape)
        if multivariate:
            del dim1[multivariate]
            del dim2[multivariate]
        if not np.all(dim1==dim2):
            raise Exception('x and y dimensions mismatch!')
        return y

    def check_xpred(x,x_pred,axis):
        if len(x.shape)!=len(x_pred.shape):
            x_pred = np.expand_dims(x_pred,axis=axis)
        dim1  = list(x.shape)
        dim2 = list(x_pred.shape)
        del dim1[axis]
        del dim2[axis]
        dim1
        dim2
        if not np.all(dim1==dim2):
            raise Exception('x and x_pred dimensions mismatch!')
        return x_pred

    def transpose_(V):
        m=np.arange(len(V.shape)).tolist()
        m = m[:-2] + [m[-1]] + [m[-2]]
        return V.transpose(m)

    def to_X(x,axis,multivariate):
        X = to_Y(x,axis,multivariate)
        return np.insert(X,0,1,axis = -1)

    def to_Y(x,axis,multivariate):
        m=np.arange(len(x.shape)).tolist()
        m
        try:
            m.remove(axis)
        except(ValueError):
            del m[axis]
        if multivariate:
            try:
                m.remove(multivariate)
            except(ValueError):
                del m[multivariate]
            X = np.transpose(x,m+[axis,multivariate])
        else:
            X = np.transpose(x,m+[axis])[...,np.newaxis]
        return X

    def dot_(x,y):
        if len(x.shape) > 2:
            m1 = np.arange(len(x.shape)).tolist()
            m2 = m1[:-2] + [m1[-1]] + [m1[-1]+1]
            m3 = m1[:-1] + [m1[-1]+1]
            return np.einsum(x,m1,y,m2,m3)
        else:
            return np.dot(x,y)

    x = check_var(x)
    y = check_var(y)
    x_pred = check_pred(x_pred)
    axis,multivariate = check_axis(x,axis,multivariate)
    y = check_xy(x,y,axis,multivariate)
    if x_pred is not None:
        x_pred = check_xpred(x,x_pred,axis)
        X_pred = to_X(x_pred,axis,multivariate)
    Y=to_Y(y,axis,multivariate)
    X=to_X(x,axis,multivariate)

    if len(X.shape) > 2:
        THETA=dot_(np.linalg.inv(dot_(transpose_(X),X)),dot_(transpose_(X),Y))
        if x_pred is None:
            return lambda t: dot_(to_X(t,axis,multivariate),THETA).squeeze()
        else:
            return dot_(X_pred,THETA).squeeze()
    else:
        THETA=np.linalg.inv(X.T.dot(X)).dot(X.T.dot(Y))
        if x_pred is None:
            return lambda t: to_X(t,axis,multivariate).dot(THETA)
        else:
            return x_pred.dot(THETA)

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
    def greb_folder():
        return r'/Users/dmar0022/university/phd/greb-official'

    @staticmethod
    def figures_folder():
        return constants.greb_folder()+'/figures'

    @staticmethod
    def output_folder():
        return constants.greb_folder()+'/output'

    @staticmethod
    def input_folder():
        return constants.greb_folder()+'/input'

    @staticmethod
    def scenario_2xCO2():
        return constants.output_folder()+'/scenario.exp-20.2xCO2'

    @staticmethod
    def cloud_def_file():
        return constants.greb_folder()+'/input/isccp.cloud_cover.clim'

    @staticmethod
    def solar_radiation_def_file():
        return constants.greb_folder()+'/input/solar_radiation.clim'

    @staticmethod
    def cloud_folder():
        return constants.greb_folder()+'/artificial_clouds'

    @staticmethod
    def solar_radiation_folder():
        return constants.greb_folder()+'/artificial_solar_radiation'

    @staticmethod
    def cloud_figures_folder():
        return constants.cloud_folder()+'/art_clouds_figures'

    @staticmethod
    def control_def_file():
        return constants.output_folder()+'/control.default'

    @staticmethod
    def to_greb_grid(input_cube, target_grid_cube, scheme='linear'):
        if scheme == 'linear': scheme = iris.analysis.Linear()
        elif scheme == 'nearest': scheme = iris.analysis.Nearest()
        elif scheme == 'areaweighted': scheme = iris.analysis.AreaWeighted()
        else: raise Exception('scheme must be either "linear", "nearest" or "areaweighted".')
        return input_cube.regrid(target_grid_cube,scheme)

    @staticmethod
    def shape_for_bin(type='cloud'):
        if type == 'cloud':
            # 'Shape must be in the form (tdef,ydef,xdef)'
            return (constants.dt(),constants.dy(),constants.dx())
        elif type == 'solar':
            return (constants.dt(),constants.dy(),1)
        else: raise Exception('type must be either "cloud" or "solar"')

    @staticmethod
    def to_shape_for_bin(data,type='cloud'):
        def_sh = constants.shape_for_bin(type)
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

def to_greb_indexes(lat,lon):
    if lat < -90 or lat > 90: raise Exception('GREB lat ranges between (-90 ÷ 90) degrees')
    if lon < 0 or lat > 360: raise Exception('GREB lon ranges between (0 ÷ 360) degrees')
    lat_def = constants.lat().tolist()
    lon_def = constants.lon().tolist()
    i = lat_def.index(min(lat_def, key=lambda x:abs(x-lat)))
    j = lon_def.index(min(lon_def, key=lambda x:abs(x-lon)))
    return i,j

def to_greb_time(date_str, fmt = '%y-%m-%d'):
    return dtime.strptime(date_str,fmt).toordinal()*24+24

def from_greb_time(greb_timenum,fmt = None):
    import math
    timenum = math.ceil((greb_timenum/24)-1)
    if fmt is None:
        return dtime.fromordinal(timenum)
    elif isinstance(fmt,str):
        return dtime.fromordinal(timenum).strftime(fmt)
    else:
        raise Exception('"fmt" must be either None or a valid date format')
        return

def create_clouds(time = None, longitude = None, latitude = None, value = 1,
                  cloud_base = None, outpath = None):
    '''
    - Create clouds from scratch, or by modifying an existent cloud matrix ("cloud_base").
    - Every coordinate can be specified in the form:
    - coord_name = [coord_min, coord_max] --> To apply changes only to that portion of that coordinate;
    - If coord_name = 'time', default format is '%m-%d' (The year is automatically set at 2000)
      (e.g. '03-04' for 4th March).
      To specify your own format (for month and day) use the form: [time_min,time_max,format];
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
                t_min = t_max = to_greb_time('00-'+time[0])
            else:
                t_min = t_max = int(time[0])
        elif len(time) == 2:
            if isinstance(time[0],str):
                t_min = to_greb_time('00-'+time[0])
                t_max = to_greb_time('00-'+time[1])
            else:
                t_min = int(time[0])
                t_max = int(time[1])
        elif len(time) == 3:
            if isinstance(time[0],str):
                t_min = to_greb_time('00-'+time[0],'%y-'+time[2])
                t_max = to_greb_time('00-'+time[1],'%y-'+time[2])
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
    if (isinstance(value,float) or isinstance(value,int) or isinstance(value,np.ndarray)):
        data[ind_t[:,None,None],ind_lat[:,None],ind_lon] = value
    elif callable(value):
        data[ind_t[:,None,None],ind_lat[:,None],ind_lon] = value(data[ind_t[:,None,None],ind_lat[:,None],ind_lon])
    else:
        raise Exception('"value" must be a number, numpy.ndarray or function to apply to the "cloud_base" (e.g. "lambda x: x*1.1")')
    # Correct value above 1 or below 0
    data=np.where(data<=1,data,1)
    data=np.where(data>=0,data,0)
    # Write .bin and .ctl files
    vars = {'cloud':data}
    if outpath is None:
        outpath=constants.cloud_folder()+'/cld.artificial.ctl'
    create_bin_ctl(outpath,vars)

def create_solar(time = None, latitude = None, value = 1,
                  solar_base = None, outpath = None):
    '''
    - Create solar radiation input file from scratch, or by modifying an existent
      solar radiation matrix ("solar_base").
    - Every coordinate can be specified in the form:
    - coord_name = [coord_min, coord_max] --> To apply changes only to that portion of that coordinate;
    - If coord_name = 'time', default format is '%m-%d' (The year is automatically set at 2000)
      (e.g. '03-04' for 4th March).
      To specify your own format (for month and day) use the form: [time_min,time_max,format];
    - If coord_name = 'latitude', the format is [lat_min,lat_max] in N-S degrees (-90 ÷ 90)
      (e.g. [-20,40] is from 20S to 40N);
    - "value" can be an integer, float or function to be applied element-wise to the "solar_base"
      (e.g. "lambda x: x-2.5").
    '''

    # Define constants
    def_t=constants.t()
    def_lat=constants.lat()
    dt = constants.dt()
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
                t_min = t_max = to_greb_time('00-'+time[0])
            else:
                t_min = t_max = int(time[0])
        elif len(time) == 2:
            if isinstance(time[0],str):
                t_min = to_greb_time('00-'+time[0])
                t_max = to_greb_time('00-'+time[1])
            else:
                t_min = int(time[0])
                t_max = int(time[1])
        elif len(time) == 3:
            if isinstance(time[0],str):
                t_min = to_greb_time('00-'+time[0],'%y-'+time[2])
                t_max = to_greb_time('00-'+time[1],'%y-'+time[2])
            else:
                raise Exception(t_exc)
        else:
            raise Exception(t_exc)
        ind_t=np.where((def_t>=t_min) & (def_t<=t_max))[0]
    else:
        ind_t=np.where((def_t>=def_t.min()) & (def_t<=def_t.max()))[0]
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
    if solar_base is not None:
        if isinstance(solar_base,str):
            data=data_from_binary(solar_base)['solar']
        elif isinstance(solar_base,np.ndarray):
            data = solar_base
        else:
            raise Exception('"solar_base" must be a valid .ctl or .bin file or a numpy.ndarray matrix of the solar radiation data')
        data = constants.to_shape_for_bin(data,type='solar')
    else:
        data = np.zeros((dt,dy,1))
    # Change values
    if (isinstance(value,float) or isinstance(value,int) or isinstance(value,np.ndarray)):
        data[ind_t[:,None,None],ind_lat[:,None],0] = value
    elif callable(value):
        data[ind_t[:,None,None],ind_lat[:,None],0] = value(data[ind_t[:,None,None],ind_lat[:,None],0])
    else:
        raise Exception('"value" must be a number, numpy.ndarray or function to apply to the "solar_base" (e.g. "lambda x: x-2.5")')
    # Correct value below 0
    data=np.where(data>=0,data,0)
    # Write .bin and .ctl files
    vars = {'solar':data}
    if outpath is None:
        outpath=constants.solar_radiation_folder()+'/sw.artificial.ctl'
    create_bin_ctl(outpath,vars)

def get_art_solar_filename(sc_filename):
    txt='exp-931.geoeng.'
    sc_filename = rmext(os.path.split(sc_filename)[1])
    if txt in sc_filename:
        if 'yrs' in sc_filename.split('_')[-1]:
            sc_filename = '_'.join(sc_filename.split('_')[:-1])
        art_solar_name = sc_filename[sc_filename.index(txt)+len(txt):]
        return os.path.join(constants.solar_radiation_folder(), art_solar_name)
    elif 'exp-20.2xCO2' in sc_filename:
        return constants.solar_radiation_def_file()
    else:
       raise Exception('The scenario filename must contain "exp-931.geoeng"')

def get_art_cloud_filename(sc_filename):
    txt='exp-930.geoeng.'
    sc_filename = rmext(os.path.split(sc_filename)[1])
    if txt in sc_filename:
        if 'yrs' in sc_filename.split('_')[-1]:
            sc_filename = '_'.join(sc_filename.split('_')[:-1])
        art_cloud_name = sc_filename[sc_filename.index(txt)+len(txt):]
        return os.path.join(constants.cloud_folder(), art_cloud_name)
    elif 'exp-20.2xCO2' in sc_filename:
        return constants.cloud_def_file()
    else:
       raise Exception('The scenario filename must contain "exp-930.geoeng"')

def get_scenario_filename(filename,years=50):
    txt1='cld.artificial'
    txt2='sw.artificial'
    filename = rmext(filename)
    filename_ = os.path.split(filename)[1]
    if txt1 in filename_:
        sc_name = 'scenario.exp-930.geoeng.'+filename_+'_{}yrs'.format(years)
    elif txt2 in filename_:
        sc_name = 'scenario.exp-931.geoeng.'+filename_+'_{}yrs'.format(years)
    elif (filename == constants.cloud_def_file()) or (filename == constants.solar_radiation_def_file()):
        sc_name = 'scenario.exp-20.2xCO2'+'_{}yrs'.format(years)
    else:
       raise Exception('The forcing file must contain either "cld.artificial" or "sw.artificial"')
    return os.path.join(constants.output_folder(),sc_name)

def input_(def_input,argv=1):
    if (argv < 1 or np.all([not isinstance(argv,int),not isinstance(argv,np.int64),not isinstance(argv,np.int32)])):
        raise Exception('argv must be an integer greater than 0')
    try:
        input=sys.argv[argv]
        if ((argv == 1 and input == '-f') or (argv==2 and os.path.splitext(input)[1]=='.json')):
            return rmext(def_input) if isinstance(def_input,str) else def_input
        else:
            return rmext(input) if isinstance(def_input,str) else type(def_input)(input)
    except(IndexError): return rmext(def_input) if isinstance(def_input,str) else def_input

def plot_clouds(filename,filename_base = None,outpath=None):
    from random import randint
    from datetime import timedelta

    fl=False
    if filename_base is not None:
        fl=True
        data_base=cube_from_binary(filename_base)
        name_base=os.path.split(rmext(filename_base))[1]

    data=cube_from_binary(filename)
    name=os.path.split(rmext(filename))[1]
    if outpath is not None:
        outpath=os.path.join(outpath,name)
        os.makedirs(outpath,exist_ok=True)
        if fl:
            outpath_diff=os.path.join(outpath,name,'diff_'+name_base)
            os.makedirs(outpath_diff,exist_ok=True)
    else:
        outpath_diff = None



    # Plot annual data
    plt.figure()
    plot_param.from_cube(data).to_annual_mean().assign_var().plot(outpath = outpath,
                            coast_param = {'edgecolor':[0,.5,0.3]},statistics=True)
    if fl:
        plt.figure()
        plot_param.from_cube(data).to_annual_mean().to_anomalies(data_base).assign_var().plot(outpath = outpath_diff,
                                coast_param = {'edgecolor':[0,.5,0.3]},statistics=True)

    # Plot seasonal cycle datad
    plt.figure()
    plot_param.from_cube(data).to_seasonal_cycle().assign_var().plot(outpath = outpath,
                            coast_param = {'edgecolor':[0,.5,0.3]},statistics=True)
    if fl:
        plt.figure()
        plot_param.from_cube(data).to_seasonal_cycle().to_anomalies(data_base).assign_var().plot(outpath = outpath_diff,
                                coast_param = {'edgecolor':[0,.5,0.3]},statistics=True)
    # Plot time data over 3 points (to check seasonality and general diagnostic)
    P = [(42,12.5),(-37.8,145),(-80,0),(0,230)]
    for p in P:
        plt.figure()
        if fl:
            plot_annual_cycle(p,data,data_base,title = 'Cloud annual cycle',name = 'cloud')
        else:
            plot_annual_cycle(p,data,title = 'Cloud annual cycle',name = 'cloud')

    os.remove(filename+'.nc')
    if filename_base is not None: os.remove(filename_base+'.nc')

def ignore_warnings():
# Ignore warnings
    if not sys.warnoptions:
        warnings.simplefilter("ignore")

def cube_from_binary(filename):
    filename = rmext(filename)
    bin2netCDF(filename)
    cube=parsevar(iris.load(filename+'.nc'))
    if len(cube) == 1:
        return iris.util.squeeze(cube[0])
    else:
        return [iris.util.squeeze(x) for x in cube]

def data_from_binary(filename,flag='raw'):
    # 1st version, quicker but not precise on time corrections
    '''
    The flag can be:
    "raw" --> no corrections are performed on the data
    "correct_units" --> units correction is performed for some variables ("precip","eva" and "qcrcl")
    "monthly" --> time correction is performed so that data belonging to the same MONTH will be averaged
    "daily" --> time correction is performed so that data belonging to the same DAY OF THE YEAR will be averaged
    "correct_all" (default) --> correct both time values and units
    '''
    # CHECK FLAGS
    if flag not in ['raw','correct_units','monthly','daily','correct_all']:
        raise Exception('Flag must be one of the following:\n"raw","correct_units","monthly","daily","correct_all"')
    # If flag is not "raw" use data_from_binary_2 (more precise)
    def data_from_binary_2(filename,flag='correct_all'):
    # 2nd version, slower but precise on time corrections
        filename = rmext(filename)
        bin2netCDF(filename)
        data = iris.load(filename+'.nc')
        if flag in ['correct_units','correct_all']:
            data = parsevar(data)
        keys = [d.var_name for d in data]
        if flag == 'monthly':
            for d in data: iris.coord_categorisation.add_month(d, 'time', name='month')
            data = [d.aggregated_by('month',iris.analysis.MEAN) for d in data]
        elif flag in ['daily','correct_all']:
            for d in data: iris.coord_categorisation.add_day_of_year(d, 'time', name='day_of_year')
            data = [d.aggregated_by('day_of_year',iris.analysis.MEAN) for d in data]
        vals = [d.data.data.squeeze() for d in data]
        dic = dict(zip(keys,vals))
        os.remove(filename+'.nc')
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

def create_ctl(path, varnames = None, xdef = None,
               ydef = None, zdef = 1, tdef = None):
    path = rmext(path)
    if not isinstance(varnames,list): varnames = [varnames]
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
    varvals = [constants.to_shape_for_bin(v,type=n) for v,n in zip(varvals,varnames)]
    varvals=[np.float32(v.copy(order='C')) for v in varvals]
    tdef,ydef,xdef = varvals[0].shape

    # WRITE CTL FILE
    create_ctl(path, varnames = varnames, xdef=xdef,ydef=ydef,tdef=tdef)
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
    # compute annual mean
    amean=[iris.util.squeeze(var.collapsed('time',iris.analysis.MEAN)) \
                                                            for var in cubes]
    return amean[0] if fl else amean

def seasonal_cycle(cubes):
    # Create seasonal cycle (DJF-JJA)
    fl=False
    if not isinstance(cubes,list):
        cubes = [cubes]
        fl=True
    metadata = [cube.metadata for cube in cubes]
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
    for c,m in zip(cycle,metadata):
        c.metadata =  m
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
            d.metadata = cubes[i].metadata
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

def global_mean(data):
    if not isinstance(data,iris.cube.Cube): raise Exception('data must an iris.cube.Cube object')
    coords=[d.standard_name for d in data.dim_coords]
    shp=list(data.data.shape)
    has_lat = ('latitude' in coords)
    has_lon = ('longitude' in coords)
    if has_lat:
        weights=np.cos(np.deg2rad(data.coord('latitude').points))
        indla =  coords.index('latitude')
        nones=[None for _ in shp]
        nones[indla]=...
        shp[indla]=1
        weights=np.tile(weights[nones], shp)
        if has_lon:
            gmean = iris.util.squeeze(data.collapsed(('latitude','longitude'),iris.analysis.MEAN,weights=weights))
        else:
            gmean = iris.util.squeeze(data.collapsed('latitude',iris.analysis.MEAN,weights=weights))
    else:
        if has_lon:
            gmean = iris.util.squeeze(data.collapsed('longitude',iris.analysis.MEAN))
        else:
            gmean = data
    return gmean

class plot_param:
    ext = 'png'
    defvar = ['tatmos','tsurf','tocean','precip','eva','qcrcl','vapor','ice','cloud','solar']
    defflags = ['amean','seascyc','anom']

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
             colorbar_param = {},
             save_param = {'dpi':300, 'bbox_inches':'tight'},
             statistics=True):
        # plt.figure(figsize=(12, 8))
        plt.axes(projection=projection) if ax is None else plt.axes(ax)
        try:
            iplt.contourf(self.get_cube(), levels = self.get_cmaplev(), cmap = self.get_cmap(),
                          extend=self.get_cbextmode())
        except:
            print('{} could not be plotted due to a contour plot error\n'.format(self.get_varname()))
            return
        plt.gca().add_feature(cfeature.COASTLINE,**coast_param)
        if self.get_defname() == 'tocean':
            plt.gca().add_feature(cfeature.NaturalEarthFeature('physical',
                                                  'land', '110m', **land_param))
        plt.colorbar(orientation='horizontal', extend=self.get_cbextmode(),
                     label=self.get_units(), ticks=self.get_cbticks(),**colorbar_param)
        plt.title(self.get_tit(),**title_param)
        if statistics:
            txt = ('gmean = {:.3f}'+'\n'+'rms = {:.3f}').format(self.gmean(),self.rms())
            # txt = ('gmean = {:.3f}'+'\n'+\
            #       'std = {:.3f}'+'\n'+\
            #       'rms = {:.3f}').format(self.gmean(),self.std(),self.rms())
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
        if self.varname is None: self.varname = 'unknown'
        self.set_varname(self.varname+'.amean')
        if tit is None:
            self.set_tit(self.get_varname())
        self.add_flags('amean')
        return self

    def to_seasonal_cycle(self):
        tit = self.get_tit()
        cube = self.get_cube()
        newcube = seasonal_cycle(cube)
        self.set_cube(newcube)
        if self.varname is None: self.varname = 'unknown'
        self.set_varname(self.varname+'.seascyc')
        if tit is None:
            self.set_tit(self.get_varname())
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
        return (global_mean(self.get_cube())).data

    def rms(self):
        return np.sqrt((global_mean(self.get_cube()**2)).data)


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
                self.set_cmaplev(np.arange(-2,2+0.2,0.2))
                self.set_cbticks(np.arange(-2,2+0.4,0.4))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-2,2+0.2,0.2))
                self.set_cbticks(np.arange(-2,2+0.4,0.4))
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
                self.set_cmaplev(np.arange(-2,2+0.2,0.2))
                self.set_cbticks(np.arange(-2,2+0.4,0.4))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-2,2+0.2,0.2))
                self.set_cbticks(np.arange(-2,2+0.4,0.4))
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
                self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                self.set_cbticks(np.arange(-1,1+0.2,0.2))
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
                self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                self.set_cbticks(np.arange(-1,1+0.2,0.2))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                self.set_cbticks(np.arange(-1,1+0.2,0.2))
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
                self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                self.set_cbticks(np.arange(-1,1+0.2,0.2))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                self.set_cbticks(np.arange(-1,1+0.2,0.2))
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
                self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                self.set_cbticks(np.arange(-1,1+0.2,0.2))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                self.set_cbticks(np.arange(-1,1+0.2,0.2))
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
                self.set_cmaplev(np.arange(-0.5,0.5+0.05,0.05))
                self.set_cbticks(np.arange(-0.5,0.5+0.1,0.1))
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-0.5,0.5+0.05,0.05))
                self.set_cbticks(np.arange(-0.5,0.5+0.1,0.1))
        else:
            if 'amean' in flags:
                self.set_cmaplev(np.arange(0,1+0.05,0.05))
                self.set_cbticks(np.arange(0,1+0.1,0.1))
                self.set_cbextmode('neither')
            elif 'seascyc' in flags:
                self.set_cmaplev(np.arange(-1,1+0.1,0.1))
                self.set_cbticks(np.arange(-1,1+0.2,0.2))
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
