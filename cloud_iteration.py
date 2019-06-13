# LIBRARIES
from greb_climatevar import * # Import self defined classes and function
ignore_warnings()

# define files
control_fname = constants.control_def_file()
t_old_init_fname = '/Users/dmar0022/university/phd/greb-official/output/scenario.exp-20.2xCO2'
t_new_init_fname = '/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1'
cld_old_init_fname = constants.cloud_file()
cld_new_init_fname = get_art_cloud_filename(t_new_init_fname)

a=iter(np.arange(1,100))
t_new_fname = input_(t_new_init_fname,next(a))
cld_new_fname = input_(cld_new_init_fname,next(a))
niter=input_(1,next(a))
time = input_('monthly',next(a))

t=lambda fn,t: data_from_binary(fn,t)['tsurf']
cld=lambda cl,t: data_from_binary(cl,t)['cloud']

cld_base = cld(cld_new_fname,'raw')
#========================================================================== #
# MONTHLY DATA
if time == 'monthly':
    mdays=np.array([31,28,31,30,31,30,31,31,30,31,30,31])
    dT = t(t_new_init_fname,'monthly')-t(t_old_init_fname,'monthly')
    dCLD = cld(cld_new_init_fname,'monthly')-cld(cld_old_init_fname,'monthly')
    t_new = t(t_new_fname,'monthly')
    t_c = t(control_fname,'monthly')

    r_cld = dCLD/dT
    dCLD_new = -r_cld*(t_new-t_c)
    dCLD_new=np.repeat(dCLD_new,mdays*2,axis=0)
# #========================================================================== #
# # ANNUAL MEAN DATA
elif time == 'annual':
    dT = t(t_new_init_fname,'raw').mean(axis=0)-t(t_old_init_fname,'raw').mean(axis=0)
    dCLD = cld(cld_new_init_fname,'raw').mean(axis=0)-cld(cld_old_init_fname,'raw').mean(axis=0)
    t_new = t(t_new_fname,'raw').mean(axis=0)
    t_c = t(control_fname,'raw').mean(axis=0)

    r_cld = dCLD/dT
    dCLD_new = -r_cld*(t_new-t_c)
# #========================================================================== #
else:
    raise Exception('Time must be either "monthly" or "annual"')

new_cloud = dCLD_new+cld_base
new_name = '/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.iter{}_{}'.format(niter,time)
create_clouds(value = new_cloud,cloud_base=None, outpath=new_name)
