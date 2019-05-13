from greb_climatevar import *

# create_ctl('/Users/dmar0022/university/phd/greb-official/input/cld_artificial.ctl')

mtx = np.zeros((730,96,48),dtype = np.float32)
path='/Users/dmar0022/university/phd/greb-official/input/cld_artificial.ctl'
vars = {'cloud':mtx}

create_bin_ctl(path,vars)
