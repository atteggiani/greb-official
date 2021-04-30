import warnings
warnings.simplefilter("ignore")
from myfuncs import GREB as greb
import xarray as xr
from scipy.ndimage import gaussian_filter
import numpy as np
import os

input_folder="/Users/dmar0022/university/phd/greb-official/S_sensitivity/solar/temp"
S=xr.open_mfdataset(os.path.join(input_folder,
                "S.lat.*"),parallel=True).S                
S.attrs={}
S.attrs["long_name"]="S" 
S.attrs["units"]="K/(Wm-2)" 

# CORRECTION FOR VERY HIGH VALUES OF S (SMALL VALUES OF SW_CTL)
S=S.where(S<1,0)
# CORRECTION FOR VERY SMALL VALUES OF S (HIGH VALUES OF SW_CTL)
S=S.where(S>1e-4,0)

# SMOOTHING
Ssm=greb.def_DataArray(dims=["time","lat","lon"],coords={"time":np.arange(1,13),"lat":greb.lat(),"lon":greb.lon()})
S_tiled=np.tile(S,(1,1,3))
for i,_ in enumerate(S.time):
   Ssm[i,...]=gaussian_filter(S_tiled[i,...],sigma=[1,2])[:,greb.dx():greb.dx()*2]
# TIME INTERPOLATION
Sint=Ssm.interp(time=np.linspace(S.time[0],S.time[-1],730),method='linear').assign_coords(time=greb.t())

# WRITE bin/ctl file
greb.create_bin_ctl(os.path.join(greb.greb_folder(),'S_sensitivity/solar/Ssw'),{'S':Sint})
