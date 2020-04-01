from myfuncs import *
import matplotlib
ignore_warnings()

# 2) Run one with 4xCO2 + fixed Tsurf (keep that of the control)
# 3) Run a geoeng experiment (SW) with 4xCO2 with iteration to minimize response
# 4) Run GREB exp with fixed Tsurf to be the residual patterns of exp3.
# 5) Replicate ricke et al experiment using their CO2 concentration

#
# for a in np.arange(0.95,0.976+0.002,0.002):
#     create_solar(solar_base=constants.solar_def_file(), value=lambda x: x*a,
#                  outpath=constants.solar_folder()+'/sw.artificial.frominput_x{}'.format(a))

data=from_binary(constants.output_folder()+'/scenario.exp-932.geoeng.4xCO2.sw.artificial.frominput_x0.977_50yrs.bin')
data.annual_mean().anomalies().plotall(outpath='/Users/dmar0022/Desktop/data')
data_fixed=from_binary(constants.output_folder()+'/scenario.exp-933.geoeng.control-fixed.tsurf.4xCO2.sw.artificial.frominput_x0.977_50yrs.bin')
data_fixed.annual_mean().anomalies().plotall(outpath='/Users/dmar0022/Desktop/data_fixed')
