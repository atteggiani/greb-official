import warnings
warnings.simplefilter("ignore")
import myfuncs as my
from myfuncs import GREB as greb
import xarray as xr
import os
from importlib import reload
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

a=greb.from_binary("/Users/dmar0022/university/phd/greb-official/output/scenario.exp-20.2xCO2_50yrs.bin").tsurf
b=greb.from_binary("/Users/dmar0022/university/phd/greb-official/output/scenario.exp-931.geoeng.2xCO2.solar_radiation_new.clim_50yrs.bin").tsurf