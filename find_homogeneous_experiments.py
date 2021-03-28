import warnings
warnings.simplefilter("ignore")
import myfuncs as my
from myfuncs import GREB as greb
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator,FormatStrFormatter
import numpy as np
import matplotlib.cm as cm
import os

fun = lambda x: greb.from_binary(x).tsurf.annual_mean(30*12).global_mean().anomalies().values
sw_gm=fun(os.path.join(greb.output_folder(),'scenario.exp-931.geoeng.2xCO2.sw.artificial.iter20_50yrs'))
cld_gm=fun(os.path.join(greb.output_folder(),'scenario.exp-930.geoeng.2xCO2.cld.artificial.iter20_50yrs'))

# array = np.arange(0.9795,0.9796+0.00001,0.00001)
# for i in array:
#     greb.create_solar(value=lambda x: x*i,outpath=os.path.join(greb.solar_folder(),"sw.artificial.frominput_x{:.5g}".format(i)))
# [(fun("/Users/dmar0022/university/phd/greb-official/output/scenario.exp-931.geoeng.2xCO2.sw.artificial.frominput_x{:.5g}_50yrs.bin".format(i)),"{:.5g}".format(i)) for i in array]

array = np.arange(1.09091,1.09099+0.00001,0.00001)
for i in array:
    greb.create_clouds(value=lambda x: x*i,outpath=os.path.join(greb.cloud_folder(),"cld.artificial.frominput_x{:.10g}".format(i)))
[(fun("/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.2xCO2.cld.artificial.frominput_x{:.10g}_50yrs.bin".format(i)),"{:.10g}".format(i)) for i in array]
