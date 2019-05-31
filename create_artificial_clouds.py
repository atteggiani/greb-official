# =============================================================================
# FROM DEFAULT CLOUD_COVER INPUT FILE (WITH SEASONALITY) * alpha
# =============================================================================
from greb_climatevar import *
ignore_warnings()
alpha=1.1
dx = 96
dy = 48
dt = 730
filename = r'/Users/dmar0022/university/phd/greb-official/input/isccp.cloud_cover.clim.ctl'
data=data_from_binary(filename,'raw')
for key,value in data.items():
    a = value*alpha
    data[key] = np.where(a<=1,a,1)
path='/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.frominputX{}.ctl'.format(alpha)
vars = data
create_bin_ctl(path,vars)
# plot_artificial_clouds(path)

# =============================================================================
# FROM DEFAULT CLOUD_COVER INPUT FILE ANNUAL MEAN * alpha
# =============================================================================
from greb_climatevar import *
ignore_warnings()
alpha=1.1
dx = 96
dy = 48
dt = 730
filename = r'/Users/dmar0022/university/phd/greb-official/input/isccp.cloud_cover.clim.ctl'
data=data_from_binary(filename,'raw')
for key,value in data.items():
    a = value.mean(axis=0)*alpha
    data[key] = np.tile(np.where(a<=1,a,1),(dt,1,1))
path='/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.ameanX{}.ctl'.format(alpha)
vars = data
create_bin_ctl(path,vars)

# =============================================================================
# FROM DEFAULT CLOUD_COVER INPUT FILE ANNUAL MEAN
# =============================================================================
from greb_climatevar import *
ignore_warnings()
dx = 96
dy = 48
dt = 730
filename = r'/Users/dmar0022/university/phd/greb-official/input/isccp.cloud_cover.clim.ctl'
data=data_from_binary(filename,'raw')
for key,value in data.items():
    data[key] = np.tile(value.mean(axis=0),(dt,1,1))
path='/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.amean.ctl'
vars = data
create_bin_ctl(path,vars)
