from myfuncs import * # Import self defined classes and function
# define files
t_new_init_fname = constants.output_folder()+'/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1_50yrs'
t_old_init_fname = constants.scenario_2xCO2()

a=iter(np.arange(1,100))
niter=input_(1,next(a))
t_new_fname = input_(t_new_init_fname,next(a))
t_new_r_fname = input_(t_new_init_fname,next(a))
t_old_r_fname = input_(t_old_init_fname,next(a))
r_fixed_flag = input_('_nf',next(a))
cld_new_fname = constants.get_art_forcing_filename(t_new_fname,'cloud')
cld_new_r_fname = constants.get_art_forcing_filename(t_new_r_fname,'cloud')
cld_old_r_fname = constants.get_art_forcing_filename(t_old_r_fname,'cloud')

cld_base = from_binary(cld_new_fname).cloud
dT = from_binary(t_new_r_fname).anomalies(from_binary(t_old_r_fname),update_attrs=False).tsurf
t_new = from_binary(t_new_fname).tsurf
dCLD = from_binary(cld_new_r_fname,time_group='12h').anomalies(from_binary(cld_old_r_fname,time_group='12h'),update_attrs=False).cloud
t_c = from_binary(constants.control_def_file(),time_group='12h').tsurf

ny=constants.get_years_of_simulation(t_new_r_fname)
dT=dT.isel(time=slice(-12*ny-1,-1)).groupby('time.month').mean('time',keep_attrs=True).rename({'month':'time'})
t_new = t_new.isel(time=slice(-12*ny-1,-1)).groupby('time.month').mean('time',keep_attrs=True).rename({'month':'time'})
# interpolate into 12h time resolution
dT= dT.interp(time=np.linspace(dT.time[0]-0.5,dT.time[-1]+0.5,730),method='cubic',kwargs={'fill_value':'extrapolate'}).assign_coords(time=constants.t())
t_new= t_new.interp(time=np.linspace(t_new.time[0]-0.5,t_new.time[-1]+0.5,730),method='cubic',kwargs={'fill_value':'extrapolate'}).assign_coords(time=constants.t())

r_cld = dCLD/dT
dCLD_new = -r_cld*(t_new-t_c)
new_cloud = dCLD_new+cld_base

new_folder = constants.cloud_folder()+'/cld.artificial.iteration_monthly{}'.format(r_fixed_flag)
os.makedirs(new_folder,exist_ok=True)
new_name = os.path.join(new_folder,'cld.artificial.iter{}_monthly{}'.format(niter,r_fixed_flag))
create_clouds(value = new_cloud, outpath=new_name)
