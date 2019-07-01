# LIBRARIES
from greb_climatevar import *
ignore_warnings()
from scipy.signal import savgol_filter

f1 = constants.cloud_folder()+'/cld.artificial.iter1_monthly'
f2 = constants.cloud_folder()+'/cld.artificial.iter20_monthly'
f1w = constants.cloud_folder()+'/cld.artificial.iter1_monthly_weighted'
f2w = constants.cloud_folder()+'/cld.artificial.iter3_monthly_weighted'
f0 = constants.cloud_folder()+'/cld.artificial.frominput_x1.1'
fr = constants.cloud_def_file()
