from myfuncs import *
from itertools import islice
from scipy.interpolate import UnivariateSpline

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

def create_clouds_for_r(dx,dy):
    lat=constants.lat()
    lon=constants.lon()
    lat_ = np.append(lat[::dy],lat[-1])
    lon_ = np.append(lon[::dx],lon[-1])
    os.makedirs(constants.cloud_folder()+'/r_calibration',exist_ok=True)

    for l in window(lat_):
        for ll in window(lon_):
            create_clouds(latitude=l, longitude=ll,
                          cloud_base = constants.cloud_def_file(),
                          value = lambda x: x - 0.1,
                          outpath=os.path.join(constants.cloud_folder(),'r_calibration','cld.artificial.lat.{:.0f}_{:.0f}lon.{:.0f}_{:.0f}'.format(l[0],l[1],ll[0],ll[1])))
            create_clouds(latitude=l, longitude=ll,
                          time=['2000-06-01','2000-08-31'],
                          cloud_base = constants.cloud_def_file(),
                          value = lambda x: x - 0.1,
                          outpath=os.path.join(constants.cloud_folder(),'r_calibration','cld.artificial.lat.{:.0f}_{:.0f}lon.{:.0f}_{:.0f}_JJA'.format(l[0],l[1],ll[0],ll[1])))
            create_clouds(latitude=l, longitude=ll,
                          time=['2000-12-01','2000-02-28'],
                          cloud_base = constants.cloud_def_file(),
                          value = lambda x: x - 0.1,
                          outpath=os.path.join(constants.cloud_folder(),'r_calibration','cld.artificial.lat.{:.0f}_{:.0f}lon.{:.0f}_{:.0f}_DJF'.format(l[0],l[1],ll[0],ll[1])))
    print('Done!')

def create_r(dx,dy):
    lat=constants.lat()
    lon=constants.lon()
    lat_ = np.append(constants.lat()[::dy],constants.lat()[-1])
    lon_ = np.append(lon[::dx],lon[-1])

    # initialize r
    r = constants.def_DataArray(dims=('time','lat','lon'),coords={'time':np.arange(1,13),'lat':constants.lat(),'lon':constants.lon()})
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

            dt=(from_binary(fname) - from_binary(fname_control)).tsurf
            dt_JJA=(from_binary(fname_JJA) - from_binary(fname_control)).tsurf
            dt_DJF=(from_binary(fname_DJF) - from_binary(fname_control)).tsurf

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

            r=r.where(~mask,dcld/dt)
            r=r.where(~mask_JJA,dcld_JJA/dt_JJA)
            r=r.where(~mask_DJF,dcld_DJF/dt_DJF)

            # for _ in [1,2]:
            #     spl=UnivariateSpline(x,DataArray(r).sel(lat=slice(l[0],l[1]),lon=slice(ll[0],ll[1])).global_mean(),s=0.002)
            #     new=spl(x)
            #     r=r.where(~(mask_lat&mask_lon&~(r.time == 0)),np.tile(new,(constants.dy(),constants.dx(),1)).transpose(2,0,1))

        create_bin_ctl(constants.greb_folder()+'/r_calibration',{'r':r.values})
        print('Done!')


# create_clouds_for_r(dx,dy)
create_r(dx,dy)


select=lambda x: x.sel(lat=slice(l[0],l[1]),lon=slice(ll[0],ll[1]))
DataArray(select(r)).annual_mean().plot()
DataArray(r).global_mean().plot()

r_load=from_binary(constants.greb_folder()+'/r_calibration').r
r_load.annual_mean().plot()


# # PLOT R
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
