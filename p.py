from myfuncs import *
import numpy as np



d=from_binary("/Users/dmar0022/university/phd/greb-official/artificial_solar_radiation/sw.artificial.iteration/sw.artificial.iter20.bin").solar
d.annual_mean().anomalies().plotvar(
            levels=np.linspace(-20,0,100),
            cbar_kwargs={"ticks":np.arange(-20,1,2)},
            cmap=cm.hsv,
            # outpath="/Users/dmar0022/university/phd/greb-official/figures/scenario.exp-931.geoeng.sw.artificial.iteration_50yrs_0.2corr/iter20/diff_control.default/data.amean.anom.png",
            )

d.seasonal_cycle().anomalies().plotvar(
            outpath="/Users/dmar0022/university/phd/greb-official/figures/scenario.exp-931.geoeng.sw.artificial.iteration_50yrs_0.2corr/iter20/diff_control.default/data.seascyc.anom.png",
            )
