# LIBRARIES
from greb_climatevar import * # Import self defined classes and function
ignore_warnings()
from scipy.signal import savgol_filter

# define files
control_fname = constants.control_def_file()
t_new_init_fname = constants.output_folder()+'/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1'
t_old_init_fname = constants.output_folder()+'/scenario.exp-20.2xCO2'

a=iter(np.arange(1,100))
niter=input_(1,next(a))
time = input_('monthly',next(a))
t_new_fname = input_(t_new_init_fname,next(a))
t_new_r_fname = input_(t_new_init_fname,next(a))
t_old_r_fname = input_(t_old_init_fname,next(a))
cld_new_fname = get_art_cloud_filename(t_new_fname)
cld_new_r_fname = get_art_cloud_filename(t_new_r_fname)
cld_old_r_fname = get_art_cloud_filename(t_old_r_fname)

t=lambda fn,t: data_from_binary(fn,t)['tsurf']
cld=lambda cl,t: data_from_binary(cl,t)['cloud']
cld_base = cld(cld_new_fname,'raw')

if 'monthly' in time.split('_'):
    tt = 'monthly'
elif 'annual' in time.split('_'):
    tt = 'raw'
else:
    raise Exception('Time must contain either "monthly" or "annual"')

dT = t(t_new_r_fname,'raw')-t(t_old_r_fname,'raw')
dCLD = cld(cld_new_r_fname,'monthly')-cld(cld_old_r_fname,'monthly')
t_new = t(t_new_fname,'raw')
t_c = t(control_fname,'raw')

ny=1
dT=dT[-(12*ny):,...].reshape([ny,12,48,96]).mean(axis=0)
t_new=t_new[-(12*ny):,...].reshape([ny,12,48,96]).mean(axis=0)

if tt == 'raw':
    dT = dT.mean(axis=0)
    dCLD = dCLD.mean(axis=0)
    t_new = t_new.mean(axis=0)
    t_c = t_c.mean(axis=0)

r_cld = dCLD/dT
dCLD_new = -r_cld*(t_new-t_c)

if tt == 'monthly':
    mdays=np.array([31,28,31,30,31,30,31,31,30,31,30,31])
    dCLD_new=np.repeat(dCLD_new,mdays*2,axis=0)

new_cloud = dCLD_new+cld_base
new_cloud=savgol_filter(new_cloud, 29,3,axis = 0,mode='mirror')
new_cloud=savgol_filter(new_cloud, 55,3,axis = 0,mode='mirror')
new_cloud=savgol_filter(new_cloud, 61,3,axis = 0,mode='mirror')

new_name = constants.cloud_folder()+'/cld.artificial.iter{}_{}'.format(niter,time)
create_clouds(value = new_cloud,cloud_base=None, outpath=new_name)
