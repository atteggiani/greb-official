from myfuncs import *

cld=from_binary(constants.cloud_folder()+'/cld.artificial.iteration_monthly_nf_ocean/cld.artificial.iter2_monthly_nf_ocean.bin').cloud
cld.annual_mean().anomalies().plotvar()
