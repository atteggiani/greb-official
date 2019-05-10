import os
import sys
from cdo import *


filename = os.path.splitext(sys.argv[1])[0] if os.path.splitext(sys.argv[1])[1] in ['.bin','.ctl'] else sys.argv[1]
if not os.path.isfile(filename+'.nc'):
    # Converting bin file to netCDF
    cdo = Cdo() # Initialize CDO
    cdo.import_binary(input = filename+'.ctl', output = filename+'.nc', options = '-f nc')
