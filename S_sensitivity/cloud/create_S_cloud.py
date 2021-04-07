import warnings
warnings.simplefilter("ignore")
from argparse import ArgumentParser
from myfuncs import GREB as greb
import numpy as np
import os 
from itertools import islice,product as iproduct, count, repeat
import concurrent.futures as cf
import time
import xarray as xr

# import myfuncs as my 
# from scipy.interpolate import griddata
# import matplotlib.pyplot as plt
# import matplotlib.cm as cm


## PARSE ARGUMENTS
# parser=ArgumentParser()
# parser.add_argument('--nlat',type=int,default=10)
# parser.add_argument('--nlon',type=int,default=20)
# parser.add_argument('-y','--years',type=int,default=30)
# args=parser.parse_args()
# nlat=args.nlat
# nlon=args.nlon
# years=args.years
nlat,nlon,years=10,20,30

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

def main(bound):
    l,ll = bound[0],bound[1]
    cld_name='cld.artificial.lat.{:.0f}_{:.0f}lon.{:.0f}_{:.0f}'.format(l[0],l[1],ll[0],ll[1])
    cld_name_DJF='_'.join([cld_name,'DJF'])
    cld_name_MAM='_'.join([cld_name,'MAM'])
    cld_name_JJA='_'.join([cld_name,'JJA'])
    cld_name_SON='_'.join([cld_name,'SON'])

    fname_DJF=greb.get_scenario_filename(cld_name_DJF,years_of_simulation=int(years),input_path=greb.output_folder()+'/S_cloud')
    fname_MAM=greb.get_scenario_filename(cld_name_MAM,years_of_simulation=int(years),input_path=greb.output_folder()+'/S_cloud')
    fname_JJA=greb.get_scenario_filename(cld_name_JJA,years_of_simulation=int(years),input_path=greb.output_folder()+'/S_cloud')
    fname_SON=greb.get_scenario_filename(cld_name_SON,years_of_simulation=int(years),input_path=greb.output_folder()+'/S_cloud')

    dcld_DJF=greb.from_binary(os.path.join(greb.cloud_folder(),'S_sensitivity',cld_name_DJF)).cloud - cld_ctl
    dcld_MAM=greb.from_binary(os.path.join(greb.cloud_folder(),'S_sensitivity',cld_name_MAM)).cloud - cld_ctl
    dcld_JJA=greb.from_binary(os.path.join(greb.cloud_folder(),'S_sensitivity',cld_name_JJA)).cloud - cld_ctl
    dcld_SON=greb.from_binary(os.path.join(greb.cloud_folder(),'S_sensitivity',cld_name_SON)).cloud - cld_ctl

    dt_DJF=greb.from_binary(fname_DJF).tsurf - ctl
    dt_MAM=greb.from_binary(fname_MAM).tsurf - ctl
    dt_JJA=greb.from_binary(fname_JJA).tsurf - ctl
    dt_SON=greb.from_binary(fname_SON).tsurf - ctl

    dcld_DJF=dcld_DJF.group_by('month')
    dcld_MAM=dcld_MAM.group_by('month')
    dcld_JJA=dcld_JJA.group_by('month')
    dcld_SON=dcld_SON.group_by('month')
    dt_DJF=dt_DJF.group_by('month')
    dt_MAM=dt_MAM.group_by('month')
    dt_JJA=dt_JJA.group_by('month')
    dt_SON=dt_SON.group_by('month')

    sel_DJF = lambda x: x.sel(time=[1,2,12],lat=slice(l[0],l[1]),lon=slice(ll[0],ll[1]))
    sel_MAM = lambda x: x.sel(time=slice(3,5),lat=slice(l[0],l[1]),lon=slice(ll[0],ll[1]))
    sel_JJA = lambda x: x.sel(time=slice(6,8),lat=slice(l[0],l[1]),lon=slice(ll[0],ll[1]))
    sel_SON = lambda x: x.sel(time=slice(9,11),lat=slice(l[0],l[1]),lon=slice(ll[0],ll[1]))
    
    S_DJF=sel_DJF(dt_DJF/dcld_DJF).roll(time=1,roll_coords=True)
    S_MAM=sel_MAM(dt_MAM/dcld_MAM)
    S_JJA=sel_JJA(dt_JJA/dcld_JJA)
    S_SON=sel_SON(dt_SON/dcld_SON)

    S=xr.concat([S_DJF,S_MAM,S_JJA,S_SON],dim="time").roll(time=-1,roll_coords=True)
    S.to_netcdf(os.path.join(output_folder,
                'S.lat.{:.0f}_{:.0f}lon.{:.0f}_{:.0f}'.format(l[0],l[1],ll[0],ll[1])))

tot=nlat*nlon
lat=greb.lat()[np.round(np.linspace(0, greb.dy() - 1, nlat+1)).astype(int)]
lon=np.append(greb.lon(),360.)[np.round(np.linspace(0, greb.dx(), nlon+1)).astype(int)]
output_folder = "/Users/dmar0022/university/phd/greb-official/S_sensitivity/cloud"
os.makedirs(output_folder,exist_ok=True)
bounds=iproduct(window(lat),window(lon))
# bounds=list(iproduct(window(lat),window(lon)))
cld_ctl=greb.from_binary(greb.cloud_def_file()).cloud
ctl=greb.from_binary(greb.scenario_2xCO2()).tsurf
n=count(1)

start=time.perf_counter()
# for bound in bounds:
#     print(f'{next(n)}/{tot}')
#     main(bound)
if __name__ == '__main__':
    with cf.ProcessPoolExecutor() as executor:
        for _ in executor.map(main, bounds, chunksize=8):
            print(f'{next(n)}/{tot}')
# S = greb.def_DataArray(data=S_data,dims=('time','lat','lon'),
#     coords={'time':np.arange(1,13),'lat':greb.lat(),'lon':greb.lon()},
#     name='S')
finish=time.perf_counter()
print(f"Execution took: {round(finish-start,2)} second(s)")


# shm.close()
# shm.unlink()
# X,Y = np.meshgrid(lat,lon)
# S_interp = S

# Sint=S.interp(time=np.linspace(S.time[0],S.time[-1],730),method='linear').assign_coords(time=greb.t())
# Sint.to_netcdf(os.path.join(greb.greb_folder(),"S_sensitivity_cloud.nc"))
# greb.create_bin_ctl(greb.greb_folder()+'/S_calibration_cloud',{'S':Sint})

# print('Interpolating...')
# for n,t in list(enumerate(S.time)):
#     print(n)
#     values=[S.sel(time=t,lat=p[0],lon=p[1],method='nearest').values.tolist() for p in points]
#     S_interp[n,:,:]=griddata(points, values, (X,Y), method='cubic',).transpose()

# S_interp = greb.def_DataArray(data=S_interp,dims=('time','lat','lon'),
#                             coords={'time':np.arange(1,13),'lat':greb.lat(),'lon':greb.lon()},
#                             name='S')


# S_interp=S_interp.interp(time=np.linspace(S_interp.time[0],S_interp.time[-1],730),method='linear')
# greb.create_bin_ctl(greb.greb_folder()+'/S_calibration_cloud_interp',{'S':S_interp})


# print(f'0/{tot}',end="\r")
