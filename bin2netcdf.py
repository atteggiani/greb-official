import os
import sys
import glob
from cdo import *

filename = os.path.splitext(sys.argv[1])[0] if os.path.splitext(sys.argv[1])[1] in ['.bin','.ctl'] else sys.argv[1]
# Converting bin file to netCDF
cdo = Cdo() # Initialize CDO
cdo.import_binary(input = filename+'.ctl', output = filename+'.nc', options = '-f nc')
