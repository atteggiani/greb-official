from myfuncs import * # Import self defined classes and function

t_new_init_fname = constants.output_folder()+'/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1_50yrs'
t_old_init_fname = constants.scenario_2xCO2()

a=iter(np.arange(1,100))
niter=input_(1,next(a))
t_new_fname = input_(t_new_init_fname,next(a))
t_new_r_fname = input_(t_new_init_fname,next(a))
t_old_r_fname = input_(t_old_init_fname,next(a))
r_fixed_flag = input_('_nf',next(a))
ocean_flag = input_("",next(a))
cld_new_fname = constants.get_art_forcing_filename(t_new_fname,'cloud')
cld_new_r_fname = constants.get_art_forcing_filename(t_new_r_fname,'cloud')
cld_old_r_fname = constants.get_art_forcing_filename(t_old_r_fname,'cloud')

cld_base = from_binary(cld_new_fname).cloud
dT = (from_binary(t_new_r_fname) - from_binary(t_old_r_fname)).tsurf
t_new = from_binary(t_new_fname).tsurf
dCLD = (from_binary(cld_new_r_fname,time_group='12h') - from_binary(cld_old_r_fname,time_group='12h')).cloud

# ny=constants.get_years_of_simulation(t_new_r_fname)
ny=20
dT=dT.isel(time=slice(-12*ny-1,-1)).group_by('12h')
t_new = t_new.isel(time=slice(-12*ny-1,-1)).group_by('12h')

r_cld = dCLD/dT
dCLD_new = -r_cld*(t_new.anomalies())
# If ocean_flag is active, change clouds only over ocean
if ocean_flag is "_ocean":
    new_cloud = np.where(constants.land_ocean_mask(),dCLD_new+cld_base,cld_base)
else:
    new_cloud = dCLD_new+cld_base
# Correct clouds to be greater than equal than the default clouds (cannot reduce clouds)
def_cld=from_binary(constants.cloud_def_file()).cloud
new_cloud=np.where(new_cloud<def_cld,def_cld,new_cloud)

new_folder = constants.cloud_folder()+'/cld.artificial.iteration_monthly{}{}'.format(r_fixed_flag,ocean_flag)
os.makedirs(new_folder,exist_ok=True)
new_name = os.path.join(new_folder,'cld.artificial.iter{}_monthly{}{}'.format(niter,r_fixed_flag,ocean_flag))
create_clouds(value = new_cloud, outpath=new_name)
