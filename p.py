# LIBRARIES
from greb_climatevar import * # Import self defined classes and function
ignore_warnings()

alpha=np.arange(0.978,0.985+0.0002,0.0002)
for a in alpha:
    create_solar(value = lambda x: x*a, solar_base=constants.solar_radiation_def_file(),
    outpath = constants.solar_radiation_folder()+'/sw.artificial.frominput_x{:g}'.format(a))
