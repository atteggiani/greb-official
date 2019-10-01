from myfuncs import *

file = os.path.join(constants.cloud_folder(),'cld.artificial_best')
outpath='/Users/dmar0022/Desktop/new/'
from_binary(file).seasonal_cycle().anomalies().cloud.plotvar(outpath=outpath)
