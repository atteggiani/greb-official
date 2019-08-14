# LIBRARIES
from greb_climatevar import * # Import self defined classes and function
ignore_warnings()

sw_def=data_from_binary(constants.solar_radiation_def_file())['solar'].squeeze()
filespec=np.arange(0.974,0.98,0.0002)
