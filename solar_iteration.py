import warnings
warnings.filterwarnings("ignore")
from myfuncs import * # Import self defined classes and function

r_sw=from_binary(Constants.greb.greb_folder()+'/r_calibration_solar').r
corr = 0.2

t_init_fname = Constants.greb.output_folder()+'/scenario.exp-931.geoeng.sw.artificial.frominput_x0.98_50yrs'

a=iter(np.arange(1,100))
niter=input_(1,next(a))
t_fname = input_(t_init_fname,next(a))
ocean_flag = input_("",next(a))

folder = Constants.greb.solar_folder()+'/sw.artificial.iteration{}'.format(ocean_flag)
os.makedirs(folder,exist_ok=True)

if niter == 1:
    sw_fname = Constants.greb.get_art_forcing_filename(t_fname,'solar')
else:
    sw_fname = Constants.greb.get_art_forcing_filename(t_fname,'solar',output_path=folder)
sw_base = from_binary(sw_fname).solar

dt = from_binary(t_fname).tsurf.anomalies()

ny=1
dt = dt.isel(time=slice(-12*ny-1,-1)).group_by('12h')
dsw_new = -(corr/r_sw)*(dt)
dsw_new=dsw_new.where(r_sw!=1,0) # Correction for small r_sw
dsw_new=dsw_new.mean('lon')
# If ocean_flag is active, change clouds only over ocean
if ocean_flag is "_ocean":
    new_solar = np.where(Constants.greb.land_ocean_mask(),dsw_new+sw_base,sw_base)
else:
    new_solar = dsw_new+sw_base

# # Correct clouds to be greater than equal than the default clouds (cannot reduce clouds)
# def_cloud=from_binary(Constants.greb.cloud_def_file()).cloud
# new_cloud=new_cloud.where(new_cloud>=def_cloud,def_cloud)

new_name = os.path.join(folder,'sw.artificial.iter{}{}'.format(niter,ocean_flag))
create_solar(value = new_solar, outpath=new_name)
