from greb_climatevar import * # Import self defined classes and function
ignore_warnings()

cld_old_fname = input_('/Users/dmar0022/university/phd/greb-official/input/isccp.cloud_cover.clim.bin')
cld_new_fname = input_('/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.frominput_x1.1',2)
sc_old_fname = input_('/Users/dmar0022/university/phd/greb-official/output/scenario.exp-20.2xCO2',3)
sc_new_fname = input_('/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.cld.artificial.frominput_x1.1',4)
niter=input_(1,5)

control_fname = constants.control_def_file();
cld_old = data_from_binary(cld_old_fname)['cloud']
cld_new = data_from_binary(cld_new_fname)['cloud']
ts_c = data_from_binary(control_fname)['tsurf']
ts_old = data_from_binary(sc_old_fname)['tsurf']
ts_new = data_from_binary(sc_new_fname)['tsurf']

# annual mean
cld_old_am = cld_old.mean(axis=0)
cld_new_am = cld_new.mean(axis=0)
ts_c_am = ts_c.mean(axis=0)
ts_old_am = ts_old.mean(axis=0)
ts_new_am = ts_new.mean(axis=0)

dCLD = cld_new_am-cld_old_am
dTS = ts_new_am-ts_old_am
r_cld   = dCLD/dTS
dCLD_new = -r_cld*(ts_new_am-ts_c_am)

new_name = '/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.iter{}'.format(niter)
create_clouds(value = lambda x: x+dCLD_new,cloud_base=cld_new, outpath=new_name)
# plot_clouds(new_name)
