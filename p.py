from myfuncs import *
import matplotlib
ignore_warnings()

# 2) Run one with 4xCO2 + fixed Tsurf (keep that of the control)
# 3) Run a geoeng experiment (SW) with 4xCO2 with iteration to minimize response
# 4) Run GREB exp with fixed Tsurf to be the residual patterns of exp3.


# 2) Replicate ricke et al experiment using their CO2 concentration

data=from_binary(constants.scenario_2xCO2())
