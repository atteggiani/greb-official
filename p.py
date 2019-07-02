# LIBRARIES
from greb_climatevar import *
ignore_warnings()

name = '/cld.artificial.iter20_annual'
fn= constants.cloud_folder()+name
out=constants.cloud_folder()+'/art_clouds_figures'
plot_clouds(filename=fn,filename_base=constants.cloud_def_file(),outpath=out)

plot_clouds_and_tsurf(constants.cloud_folder()+'/cld.artificial.iter20_monthly',constants.cloud_folder()+'/cld.artificial.iter1_monthly',constants.cloud_folder()+'/cld.artificial.iter5_monthly')
