import warnings
warnings.simplefilter("ignore")
import myfuncs as my
import xarray as xr
import os
from importlib import reload
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

s=my.from_binary("/Users/dmar0022/university/phd/greb-official/artificial_solar_radiation/sw.artificial.iteration/sw.artificial.iter20.bin").solar
c=my.from_binary(my.Constants.greb.solar_def_file()).solar
a=s.anomalies()
cond1=np.logical_and(c==0,a==0)
p=my.DataArray(100*(a/c).where(~cond1,0))
pp=p.groupby("time.season").mean("time")

# DJF
plt.figure()
pp.sel(season="DJF").plotvar(
            levels=np.linspace(-10,0,100),
            cbar_kwargs={"ticks":np.arange(-10,0+1,1),"label":"%"},
            cmap=cm.gist_rainbow,
            title="SW Radiation DJF Mean Anomalies"
)
# JJA
plt.figure()
pp.sel(season="JJA").plotvar(
            levels=np.linspace(-10,0,100),
            cbar_kwargs={"ticks":np.arange(-10,0+1,1),"label":"%"},
            cmap=cm.gist_rainbow,
            title="SW Radiation JJA Mean Anomalies"
)