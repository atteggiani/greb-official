from myfuncs import *
from itertools import islice
from scipy import interpolate

dx = 4
dy = 4

def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

lat=constants.lat()
lon=constants.lon()
lat_ = np.append(constants.lat()[::dy],constants.lat()[-1])
lon_ = np.append(lon[::dx],lon[-1])

# initialize r
r = constants.def_DataArray(dims=('time','lat','lon'),
                            coords={'time':np.arange(1,13),'lat':constants.lat(),'lon':constants.lon()},
                            name='r')
t = constants.def_DataArray(dims=('time','lat','lon'),
                            coords={'time':np.arange(1,13),'lat':constants.lat(),'lon':constants.lon()},
                            name='tsurf')
a=iter(np.arange(288))
x=np.arange(1,constants.dt()+1)
for l in window(lat_):
    for ll in window(lon_):
        print('{}/288'.format(next(a)+1))
        cld_name='cld.artificial.lat.{:.0f}_{:.0f}lon.{:.0f}_{:.0f}'.format(l[0],l[1],ll[0],ll[1])
        cld_name_JJA='_'.join([cld_name,'JJA'])
        cld_name_DJF='_'.join([cld_name,'DJF'])

        fname=constants.get_scenario_filename(cld_name,years_of_simulation=20,input_path=constants.output_folder()+'/r_calibration')
        fname_control = constants.scenario_2xCO2()
        fname_JJA=constants.get_scenario_filename(cld_name_JJA,years_of_simulation=20,input_path=constants.output_folder()+'/r_calibration')
        fname_DJF=constants.get_scenario_filename(cld_name_DJF,years_of_simulation=20,input_path=constants.output_folder()+'/r_calibration')

        dcld=from_binary(os.path.join(constants.cloud_folder(),'r_calibration',cld_name)).cloud.anomalies()
        dcld_JJA=from_binary(os.path.join(constants.cloud_folder(),'r_calibration',cld_name_JJA)).cloud.anomalies()
        dcld_DJF=from_binary(os.path.join(constants.cloud_folder(),'r_calibration',cld_name_DJF)).cloud.anomalies()

        tsurf = from_binary(fname).tsurf
        tsurf_control = from_binary(fname_control).tsurf
        dt = tsurf - tsurf_control
        dt_JJA = from_binary(fname_JJA).tsurf - tsurf_control
        dt_DJF = from_binary(fname_DJF).tsurf - tsurf_control

        dcld=dcld.group_by('month')
        dcld_JJA=dcld_JJA.group_by('month')
        dcld_DJF=dcld_DJF.group_by('month')
        dt=dt.group_by('month')
        dt_JJA=dt_JJA.group_by('month')
        dt_DJF=dt_DJF.group_by('month')

        mask_lat=(r.coords['lat']>=l[0])&(r.coords['lat']<=l[1])
        mask_lon=(r.coords['lon']>=ll[0])&(r.coords['lon']<=ll[1])
        # mask_time_JJA=(r.coords['time']>=np.datetime64('2000-06-01'))&(r.coords['time']<=np.datetime64('2000-08-31'))
        # mask_time_DJF=(r.coords['time']<=np.datetime64('2000-02-28'))|(r.coords['time']>=np.datetime64('2000-12-01'))
        mask_time_JJA=(r.coords['time']>=6)&(r.coords['time']<=8)
        mask_time_DJF=(r.coords['time']<=2)|(r.coords['time']>=12)
        mask_time=~(mask_time_DJF|mask_time_JJA)

        mask=(mask_lat&mask_lon&mask_time)
        mask_JJA=(mask_lat&mask_lon&mask_time_JJA)
        mask_DJF=(mask_lat&mask_lon&mask_time_DJF)

        r=r.where(~mask,dt/dcld)
        r=r.where(~mask_JJA,dt_JJA/dcld_JJA)
        r=r.where(~mask_DJF,dt_DJF/dcld_DJF)

        t=t.where(~mask,dt)
        t=t.where(~mask_JJA,dt_JJA)
        t=t.where(~mask_DJF,dt_DJF)

r_=r.interp(time=np.linspace(r.time[0],r.time[-1],730),method='linear')
create_bin_ctl(constants.greb_folder()+'/r_calibration',{'r':r_})
r=DataArray(r)
r_.annual_mean().plotvar(cmap=cm.viridis,levels=np.arange(-10,0+0.5,0.5))

# (1/r).annual_mean().plotvar(cmap=cm.viridis,levels=np.arange(-10,0+0.5,0.5))
# (1/r).interp(time=np.linspace(r.time[0],r.time[-1],730),method='cubic').annual_mean().plotvar(cmap=cm.viridis,levels=np.arange(-10,0+0.5,0.5))
# r.global_mean().plot()

# PLOT R
# r.annual_mean().plotvar(levels=np.arange(-0.1,0+0.01,0.005),
#                         cmap=cm.viridis,
#                         name='r_annual_mean',
#                         outpath='/Users/dmar0022/Desktop')
#
# r.group_by('season').sel(time='JJA').plotvar(levels=np.arange(-0.1,0+0.01,0.005),
#                         cmap=cm.viridis,
#                         name='r_JJA',
#                         outpath='/Users/dmar0022/Desktop')
#
# r.group_by('season').sel(time='DJF').plotvar(levels=np.arange(-0.1,0+0.01,0.005),
#                         cmap=cm.viridis,
#                         name='r_DJF',
#                         outpath='/Users/dmar0022/Desktop')
