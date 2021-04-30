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

# PARSE ARGUMENTS
parser=ArgumentParser()
parser.add_argument('--nlat',type=int,default=10)
parser.add_argument('--nlon',type=int,default=20)
parser.add_argument('-y','--years',type=int,default=30)
args=parser.parse_args()
nlat=args.nlat
nlon=args.nlon
years=args.years

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
    solar_name='sw.artificial.lat.{:.0f}_{:.0f}lon.{:.0f}_{:.0f}'.format(l[0],l[1],ll[0],ll[1])
    solar_name_DJF='_'.join([solar_name,'DJF'])
    solar_name_MAM='_'.join([solar_name,'MAM'])
    solar_name_JJA='_'.join([solar_name,'JJA'])
    solar_name_SON='_'.join([solar_name,'SON'])

    fname_DJF=greb.get_scenario_filename(solar_name_DJF,years_of_simulation=int(years),input_path=greb.output_folder()+'/S_solar')
    fname_MAM=greb.get_scenario_filename(solar_name_MAM,years_of_simulation=int(years),input_path=greb.output_folder()+'/S_solar')
    fname_JJA=greb.get_scenario_filename(solar_name_JJA,years_of_simulation=int(years),input_path=greb.output_folder()+'/S_solar')
    fname_SON=greb.get_scenario_filename(solar_name_SON,years_of_simulation=int(years),input_path=greb.output_folder()+'/S_solar')

    dsw_DJF=greb.from_binary(os.path.join(greb.solar_folder(),'S_sensitivity',solar_name_DJF)).solar - sw_ctl
    dsw_MAM=greb.from_binary(os.path.join(greb.solar_folder(),'S_sensitivity',solar_name_MAM)).solar - sw_ctl
    dsw_JJA=greb.from_binary(os.path.join(greb.solar_folder(),'S_sensitivity',solar_name_JJA)).solar - sw_ctl
    dsw_SON=greb.from_binary(os.path.join(greb.solar_folder(),'S_sensitivity',solar_name_SON)).solar - sw_ctl

    dt_DJF=greb.from_binary(fname_DJF).tsurf - ctl
    dt_MAM=greb.from_binary(fname_MAM).tsurf - ctl
    dt_JJA=greb.from_binary(fname_JJA).tsurf - ctl
    dt_SON=greb.from_binary(fname_SON).tsurf - ctl

    dsw_DJF=dsw_DJF.group_by('month')
    dsw_MAM=dsw_MAM.group_by('month')
    dsw_JJA=dsw_JJA.group_by('month')
    dsw_SON=dsw_SON.group_by('month')
    dt_DJF=dt_DJF.group_by('month')
    dt_MAM=dt_MAM.group_by('month')
    dt_JJA=dt_JJA.group_by('month')
    dt_SON=dt_SON.group_by('month')

    sel_DJF = lambda x: x.sel(time=[1,2,12],lat=slice(l[0],l[1]),lon=slice(ll[0],ll[1]))
    sel_MAM = lambda x: x.sel(time=slice(3,5),lat=slice(l[0],l[1]),lon=slice(ll[0],ll[1]))
    sel_JJA = lambda x: x.sel(time=slice(6,8),lat=slice(l[0],l[1]),lon=slice(ll[0],ll[1]))
    sel_SON = lambda x: x.sel(time=slice(9,11),lat=slice(l[0],l[1]),lon=slice(ll[0],ll[1]))
    
    S_DJF=sel_DJF((dt_DJF/dsw_DJF).where(dsw_DJF!=0,0)).roll(time=1,roll_coords=True)
    S_MAM=sel_MAM((dt_MAM/dsw_MAM).where(dsw_MAM!=0,0))
    S_JJA=sel_JJA((dt_JJA/dsw_JJA).where(dsw_JJA!=0,0))
    S_SON=sel_SON((dt_SON/dsw_SON).where(dsw_SON!=0,0))

    S=xr.concat([S_DJF,S_MAM,S_JJA,S_SON],dim="time").roll(time=-1,roll_coords=True)
    S.name="S"
    S.to_netcdf(os.path.join(output_folder,
                'S.lat.{:.0f}_{:.0f}lon.{:.0f}_{:.0f}.nc'.format(l[0],l[1],ll[0],ll[1])))

tot=nlat*nlon
lat=np.linspace(-90,90, nlat+1)
lat=[-90]+[l+0.01 if l in greb.lat() else l for l in lat[1:-1]]+[90]
lon=np.linspace(0,360, nlon+1)
lon=[0]+[l+0.01 if l in greb.lon() else l for l in lon[1:-1]]+[360]
output_folder = "/Users/dmar0022/university/phd/greb-official/S_sensitivity/solar/temp"
os.makedirs(output_folder,exist_ok=True)
bounds=iproduct(window(lat),window(lon))
sw_ctl=greb.from_binary(greb.solar_def_file()).solar
ctl=greb.from_binary(greb.scenario_2xCO2()).tsurf
n=count(1)

print(f'0/{tot}',end="\r")
if __name__ == '__main__':
    with cf.ProcessPoolExecutor() as executor:
        for _ in executor.map(main, bounds):
            print(f'{next(n)}/{tot}',end="\r")
