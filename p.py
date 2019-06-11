# LIBRARIES
from greb_climatevar import * # Import self defined classes and function
ignore_warnings()

def correct(dt):
    thr_pos=lambda x: x.mean()+x.std()*4
    thr_neg=lambda x: x.mean()-x.std()*4
    thr_min=lambda x: x.std()/8
    sub_pos=lambda x: x.mean()+x.std()
    sub_neg=lambda x: x.mean()-x.std()
    d=np.array([1,1])
    while np.any([d[0]!=0,d[1]!=0]):
        m=np.array([dt.max(),dt.min()])
        dt=np.where(dt>thr_pos(dt),sub_pos(dt),dt)
        dt=np.where(dt<thr_neg(dt),sub_neg(dt),dt)
        d=np.array([dt.max(),dt.min()])-m
    dt=np.where((dt<0) & (np.abs(dt)<thr_min(dt)),-thr_min(dt),dt)
    dt=np.where((dt>=0) & (np.abs(dt)<thr_min(dt)),thr_min(dt),dt)
    return dt

cld_old_fname = input_('/Users/dmar0022/university/phd/greb-official/input/isccp.cloud_cover.clim.bin')
cld_new_fname = input_('/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.frominput_x1.1',2)
sc_old_fname = input_('/Users/dmar0022/university/phd/greb-official/output/scenario.exp-20.2xCO2',3)
sc_new_fname = input_('/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1',4)
niter=input_(1,5)

control_fname = constants.control_def_file();

#========================================================================== #
# MONTHLY DATA
mdays=np.array([31,28,31,30,31,30,31,31,30,31,30,31])
cld_old = data_from_binary(cld_old_fname,'monthly')['cloud']
cld_new = data_from_binary(cld_new_fname,'monthly')['cloud']
ts_c = data_from_binary(control_fname,'monthly')['tsurf']
ts_old = data_from_binary(sc_old_fname,'monthly')['tsurf']
ts_new = data_from_binary(sc_new_fname,'monthly')['tsurf']

dCLD = (cld_new-cld_old)
# dTS = correct(ts_new_am-ts_old_am)
dTS = ts_new-ts_old
r_cld = dCLD/dTS
dCLD_new = -r_cld*(ts_new-ts_c)
new_cloud = dCLD_new+cld_new
new_cloud=np.repeat(new_cloud,mdays*2,axis=0)

# #========================================================================== #
# # ANNUAL MEAN DATA
# cld_old = data_from_binary(cld_old_fname)['cloud']
# cld_new = data_from_binary(cld_new_fname)['cloud']
# ts_c = data_from_binary(control_fname)['tsurf']
# ts_old = data_from_binary(sc_old_fname)['tsurf']
# ts_new = data_from_binary(sc_new_fname)['tsurf']

# cld_old_am = cld_old.mean(axis=0)
# cld_new_am = cld_new.mean(axis=0)
# ts_c_am = ts_c.mean(axis=0)
# ts_old_am = ts_old.mean(axis=0)
# ts_new_am = ts_new.mean(axis=0)

# dCLD = (cld_new_am-cld_old_am)
# # dTS = correct(ts_new_am-ts_old_am)
# dTS = ts_new_am-ts_old_am
# r_cld = dCLD/dTS
# dCLD_new = -r_cld*(ts_new_am-ts_c_am)
# #========================================================================== #

new_name = '/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.iter{}_monthly'.format(niter)
# new_name = '/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.iter{}_correct'.format(niter)
# new_name = '/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.iter{}'.format(niter)
create_clouds(value = lambda x: x+dCLD_new,cloud_base=cld_new, outpath=new_name)
# plot_clouds(new_name)
