from myfuncs import *
from itertools import islice,product as iproduct
from scipy.interpolate import griddata
ignore_warnings()
dy=2
def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        return result
    for elem in it:
        result = result[1:] + (elem,)
        return result
 
def create_solar_for_r(dy=4):
    lat=constants.lat()
    lat_ = np.append(lat[::dy],lat[-1])
    folder=constants.solar_folder()+'/r_calibration'
    os.makedirs(folder,exist_ok=True)
    num=len([a for a in window(lat_)])
    n=iter(np.arange(num))
    for l in window(lat_):
        print('{}/{}'.format(next(n)+1,num))
        create_solar(latitude=l,
                     solar_base = constants.solar_def_file(),
                     value = lambda x: x - 50,
                     outpath=os.path.join(folder,'sw.artificial.lat.{:.0f}_{:.0f}'.format(l[0],l[1])))
        create_solar(latitude=l,
                     time=['2000-04-01','2000-08-31'],
                     solar_base = constants.solar_def_file(),
                     value = lambda x: x - 50,
                     outpath=os.path.join(folder,'sw.artificial.lat.{:.0f}_{:.0f}_JJA'.format(l[0],l[1])))
        create_solar(latitude=l,
                     time=['2000-10-01','2000-02-28'],
                     solar_base = constants.solar_def_file(),
                     value = lambda x: x - 50,
                     outpath=os.path.join(folder,'sw.artificial.lat.{:.0f}_{:.0f}_DJF'.format(l[0],l[1])))
    print('Done!')

# create_solar_for_r(dy)

def create_r(dy=4):
    lat=constants.lat()
    lon=constants.lon()
    lat_ = np.append(lat[::dy],lat[-1])
    # initialize r
    r = constants.def_DataArray(dims=('time','lat'),
                                coords={'time':np.arange(1,13),'lat':constants.lat()},
                                name='r')
    num=len([a for a in window(lat_)])
    a=iter(np.arange(num))
    x=np.arange(1,constants.dt()+1)
    fname_control = constants.scenario_2xCO2()
    for l in window(lat_):
        l=(84,88)
        print('{}/{}'.format(next(a)+1,num))
        sw_name='sw.artificial.lat.{:.0f}_{:.0f}'.format(l[0],l[1])
        sw_name_JJA='_'.join([sw_name,'JJA'])
        sw_name_DJF='_'.join([sw_name,'DJF'])

        fname=constants.get_scenario_filename(sw_name,years_of_simulation=20,input_path=constants.output_folder()+'/r_calibration_solar')
        fname_JJA=constants.get_scenario_filename(sw_name_JJA,years_of_simulation=20,input_path=constants.output_folder()+'/r_calibration_solar')
        fname_DJF=constants.get_scenario_filename(sw_name_DJF,years_of_simulation=20,input_path=constants.output_folder()+'/r_calibration_solar')

        dsw=from_binary(os.path.join(constants.solar_folder(),'r_calibration',sw_name)).solar.anomalies()
        dsw_JJA=from_binary(os.path.join(constants.solar_folder(),'r_calibration',sw_name_JJA)).solar.anomalies()
        dsw_DJF=from_binary(os.path.join(constants.solar_folder(),'r_calibration',sw_name_DJF)).solar.anomalies()

        dt=(from_binary(fname) - from_binary(fname_control)).tsurf
        dt_JJA=(from_binary(fname_JJA) - from_binary(fname_control)).tsurf
        dt_DJF=(from_binary(fname_DJF) - from_binary(fname_control)).tsurf

        dsw=dsw.group_by('month')
        dsw_JJA=dsw_JJA.group_by('month')
        dsw_DJF=dsw_DJF.group_by('month')
        dt=dt.group_by('month')
        dt_JJA=dt_JJA.group_by('month')
        dt_DJF=dt_DJF.group_by('month')

        mask_lat=(r.coords['lat']>=l[0])&(r.coords['lat']<=l[1])
        mask_time_JJA=(r.coords['time']>=5)&(r.coords['time']<=8)
        mask_time_DJF=(r.coords['time']<=2)|(r.coords['time']>=11)
        mask_time=~(mask_time_DJF|mask_time_JJA)

        mask=(mask_lat&mask_time)
        mask_JJA=(mask_lat&mask_time_JJA)
        mask_DJF=(mask_lat&mask_time_DJF)

        r=r.where(~mask,dt/dsw)
        r=r.where(~mask_JJA,dt_JJA/dsw_JJA)
        r=r.where(~mask_DJF,dt_DJF/dsw_DJF)

    r=r.where(r!=-np.inf,1)
    X,Y = np.meshgrid(lat,lon)
    points=list(iproduct(lat_,lon))
    r_interp=np.zeros(r.shape)
    print('Interpolating...')
    for n,t in list(enumerate(r.time)):
        print(n)
        values=[r.sel(time=t,lat=p[0],lon=p[1],method='nearest').values.tolist() for p in points]
        r_interp[n,:,:]=griddata(points, values, (X,Y), method='cubic',).transpose()

    r_interp = constants.def_DataArray(data=r_interp,dims=('time','lat','lon'),
                                coords={'time':np.arange(1,13),'lat':constants.lat(),'lon':constants.lon()},
                                name='r')

    r=r.interp(time=np.linspace(r.time[0],r.time[-1],730),method='linear')
    r_interp=r_interp.interp(time=np.linspace(r_interp.time[0],r_interp.time[-1],730),method='linear')
    create_bin_ctl(constants.greb_folder()+'/r_calibration_solar_interp',{'r':r_interp})
    create_bin_ctl(constants.greb_folder()+'/r_calibration_solar',{'r':r})
    print('Done!')

create_solar_for_r(dy)
create_r(dy)
