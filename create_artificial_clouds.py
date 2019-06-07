# =============================================================================
# FROM DEFAULT CLOUD_COVER INPUT FILE
# =============================================================================
from greb_climatevar import *
ignore_warnings()

cld_folder = os.path.join(os.getcwd(),'artificial_clouds')
cld_def = os.path.join(cld_folder,'cld.artificial.frominputX1.1')
cld=os.path.join(os.getcwd(),'artificial_clouds','cld.artificial')
mod1=os.path.join(cld_folder,'cld.artificial.frominputX1.1mod1_lat.40.-65_time.06-01.08-31.x1.1')
mod2=os.path.join(cld_folder,'cld.artificial.frominputX1.1mod2_lat.-20.20_lon.90.-170.x0.9')

name = 'cld.artificial.frominput_lat.-70.70.x1.07'
lat=[-70,70]
lon=None
time=None
val = 1.07
cld_base=constants.cloud_file()
create_clouds(latitude=lat,longitude=lon,time=time,value=lambda x: x*val,
              cloud_base=cld_base,outpath=os.path.join(cld_folder,name))
plot_clouds(os.path.join(cld_folder,name))
