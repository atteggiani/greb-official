# LIBRARIES
from greb_climatevar import * # Import self defined classes and function
ignore_warnings()

init_cld_new_fname = '/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial'
init_cld_old_fname = '/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.frominput_x1.1'
init_sc_new_fname = '/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.cld.artificial'
init_sc_old_fname = '/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1'
cld_old_fname = input_(init_cld_old_fname)
cld_new_fname = input_(init_cld_new_fname,2)
sc_old_fname = input_(init_sc_old_fname,3)
sc_new_fname = input_(init_sc_new_fname,4)
niter=input_(1,5)
time = input_('monthly',6)

control_fname = constants.control_def_file();

#========================================================================== #
# MONTHLY DATA
if time == 'monthly_fixed_2':
    mdays=np.array([31,28,31,30,31,30,31,31,30,31,30,31])
    init_cld_old = data_from_binary(init_cld_old_fname,'monthly')['cloud']
    init_cld_new = data_from_binary(init_cld_new_fname,'monthly')['cloud']
    cld_new = data_from_binary(cld_new_fname,'monthly')['cloud']
    t_c = data_from_binary(control_fname,'monthly')['tsurf']
    init_t_old = data_from_binary(init_sc_old_fname,'monthly')['tsurf']
    init_t_new = data_from_binary(init_sc_new_fname,'monthly')['tsurf']
    t_new = data_from_binary(sc_new_fname,'monthly')['tsurf']

    dCLD = init_cld_new-init_cld_old
    dT = init_t_new-init_t_old
    r_cld = dCLD/dT
    dCLD_new = -r_cld*(t_new-t_c)
    new_cloud = dCLD_new+cld_new
    new_cloud=np.repeat(new_cloud,mdays*2,axis=0)

# #========================================================================== #
# # ANNUAL MEAN DATA
if time == 'annual_fixed_2':
    init_cld_old = data_from_binary(init_cld_old_fname)['cloud']
    init_cld_new = data_from_binary(init_cld_new_fname)['cloud']
    cld_new = data_from_binary(cld_new_fname)['cloud']
    t_c = data_from_binary(control_fname)['tsurf']
    init_t_old = data_from_binary(init_sc_old_fname)['tsurf']
    init_t_new = data_from_binary(init_sc_new_fname)['tsurf']
    t_new = data_from_binary(sc_new_fname)['tsurf']

    init_cld_old_am = init_cld_old.mean(axis=0)
    init_cld_new_am = init_cld_new.mean(axis=0)
    t_c_am = t_c.mean(axis=0)
    init_t_old_am = init_t_old.mean(axis=0)
    init_t_new_am = init_t_new.mean(axis=0)
    t_new_am = t_new.mean(axis=0)

    dCLD = (init_cld_new_am-init_cld_old_am)
    dT = init_t_new_am-init_t_old_am
    r_cld = dCLD/dT
    dCLD_new = -r_cld*(t_new_am-t_c_am)
    new_cloud = dCLD_new+cld_new

# #========================================================================== #

new_name = '/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.iter{}_{}'.format(niter,time)
create_clouds(value = new_cloud,cloud_base=None, outpath=new_name)
