# LIBRARIES
from greb_climatevar import *
ignore_warnings()

cloudfiles = [constants.cloud_folder()+'/cld.artificial.iter20_monthly_20y_nf',
              constants.cloud_folder()+'/cld.artificial.iter1_monthly_20y_nf']

plot_clouds_and_tsurf(*cloudfiles)
