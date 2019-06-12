# LIBRARIES
from greb_climatevar import * # Import self defined classes and function
ignore_warnings()

cld_old_fname = input_('/Users/dmar0022/university/phd/greb-official/input/isccp.cloud_cover.clim.bin')
cld_new_fname = input_('/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.frominput_x1.1',2)
sc_old_fname = input_('/Users/dmar0022/university/phd/greb-official/output/scenario.exp-20.2xCO2',3)
sc_new_fname = input_('/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1',4)
niter=input_(1,5)
time = input_('monthly',6)

control_fname = constants.control_def_file();

#========================================================================== #
# MONTHLY DATA
if time == 'monthly':
    mdays=np.array([31,28,31,30,31,30,31,31,30,31,30,31])
    cld_old = data_from_binary(cld_old_fname,'monthly')['cloud']
    cld_new = data_from_binary(cld_new_fname,'monthly')['cloud']
    t_c = data_from_binary(control_fname,'monthly')['tsurf']
    t_old = data_from_binary(sc_old_fname,'monthly')['tsurf']
    t_new = data_from_binary(sc_new_fname,'monthly')['tsurf']

    dCLD = (cld_new-cld_old)
    dT = t_new-t_old
    r_cld = dCLD/dT
    dCLD_new = -r_cld*(t_new-t_c)
    new_cloud = dCLD_new+cld_new
    new_cloud=np.repeat(new_cloud,mdays*2,axis=0)

# #========================================================================== #
# # ANNUAL MEAN DATA
if time == 'annual':
    cld_old = data_from_binary(cld_old_fname)['cloud']
    cld_new = data_from_binary(cld_new_fname)['cloud']
    t_c = data_from_binary(control_fname)['tsurf']
    t_old = data_from_binary(sc_old_fname)['tsurf']
    t_new = data_from_binary(sc_new_fname)['tsurf']

    cld_old_am = cld_old.mean(axis=0)
    cld_new_am = cld_new.mean(axis=0)
    t_c_am = t_c.mean(axis=0)
    t_old_am = t_old.mean(axis=0)
    t_new_am = t_new.mean(axis=0)

    dCLD = (cld_new_am-cld_old_am)
    dT = t_new_am-t_old_am
    r_cld = dCLD/dT
    dCLD_new = -r_cld*(t_new_am-t_c_am)
    new_cloud = dCLD_new+cld_new
