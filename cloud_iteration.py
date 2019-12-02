from myfuncs import * # Import self defined classes and function

r_cld=from_binary(constants.greb_folder()+'/r_calibration').r
# r_cld=from_binary('/Users/dmar0022/Desktop/dietmar_script/data/greb.cloud.sensitivity.best-guess.gad').rcld
# r_cld.coords['time']=np.arange(1,13)
# r_cld=r_cld.interp(time=np.linspace(1,12,730),method='linear')
# r_cld.coords['time']=constants.t()

corr = 0.1 #correction factor (0.1 for my r_cld, 0.2 for dietmar's)

t_init_fname = constants.output_folder()+'/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1_50yrs'

a=iter(np.arange(1,100))
niter=input_(1,next(a))
t_fname = input_(t_init_fname,next(a))
ocean_flag = input_("",next(a))

folder = constants.cloud_folder()+'/cld.artificial.iteration{}'.format(ocean_flag)
os.makedirs(folder,exist_ok=True)

if niter == 1:
    cld_fname = constants.get_art_forcing_filename(t_fname,'cloud')
else:
    cld_fname = constants.get_art_forcing_filename(t_fname,'cloud',output_path=folder)
cld_base = from_binary(cld_fname).cloud

dt = from_binary(t_fname).tsurf.anomalies()

ny=1
dt = dt.isel(time=slice(-12*ny-1,-1)).group_by('12h')
dCLD_new = -(corr/r_cld)*(dt)
dCLD_new=dCLD_new.where(np.abs(r_cld)>=1,0) # Correction for small r_cld
# If ocean_flag is active, change clouds only over ocean
if ocean_flag is "_ocean":
    new_cloud = np.where(constants.land_ocean_mask(),dCLD_new+cld_base,cld_base)
else:
    new_cloud = dCLD_new+cld_base
# Correct clouds to be greater than equal than the default clouds (cannot reduce clouds)
# def_cld=from_binary(constants.cloud_def_file()).cloud
# new_cloud=np.where(new_cloud<def_cld,def_cld,new_cloud)

new_name = os.path.join(folder,'cld.artificial.iter{}{}'.format(niter,ocean_flag))
create_clouds(value = new_cloud, outpath=new_name)
