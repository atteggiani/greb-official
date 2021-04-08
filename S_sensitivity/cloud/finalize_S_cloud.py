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
import myfuncs as my

input_folder="/Users/dmar0022/university/phd/greb-official/S_sensitivity/cloud/temp"
S=xr.open_mfdataset(os.path.join(input_folder,
                "S.lat.*"),parallel=True).__xarray_dataarray_variable__
S.name="S"
S.attrs={}
S.attrs["long_name"]="S" 
S.attrs["units"]="" 


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
