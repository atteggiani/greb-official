import warnings
warnings.simplefilter("ignore")
from myfuncs import GREB as greb
import myfuncs as my
import numpy as np
from itertools import islice,product as iproduct, count
import concurrent.futures as cf
import time
import os
from argparse import ArgumentParser
import matplotlib.cm as cm

a=greb.from_binary("/Users/dmar0022/university/phd/greb-official/output/scenario.exp-931.geoeng.2xCO2.sw.artificial.iter5_0.3corr_50yrs.bin")


a.tsurf.annual_mean().anomalies().plotvar(levels=np.linspace(-1,1,50),du=0.2,
    outpath=os.path.join(greb.figures_folder(),"sw_iter5_0.3corr_tsurf.png"))

a.precip.annual_mean().anomalies().plotvar(levels=np.linspace(-0.5,0.5,50),du=0.25,
    outpath=os.path.join(greb.figures_folder(),"sw_iter5_0.3corr_precip.png"))    