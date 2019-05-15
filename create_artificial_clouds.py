# =============================================================================
# FROM DEFAULT CLOUD_COVER INPUT FILE (ANNUAL MEAN)
# =============================================================================
from greb_climatevar import *
ignore_warnings()
dx = 96
dy = 48
dt = 730
filename = r'/Users/dmar0022/university/phd/greb-official/input/isccp.cloud_cover.clim.ctl'
data=data_from_input(filename)
for key,value in data.items():
    data[key] = np.tile(value.mean(axis=0),(dt,1,1))
path='/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.amean.ctl'
vars = data
create_bin_ctl(path,vars)
plot_artificial_clouds(path)
# =============================================================================
# FROM SCRATCH
# =============================================================================
from greb_climatevar import *
ignore_warnings()

dt = 730
dx = 96
dy = 48

path='/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.all0.ctl'

mtx = np.ones((dx,dy,dt))
vars = {'cloud':mtx}
create_bin_ctl(path,vars)
plot_artificial_clouds(path)
