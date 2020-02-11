from myfuncs import *
import matplotlib
ignore_warnings()

# 1) Make the cloud figures as the r_cld ones (without the default clouds)
# 2) Develop an experiment with locally changing Solar Radiation (similar to the cloud one)

nlev=200
cmap_tsurf=constants.colormaps.Div_tsurf()
cmap_precip=constants.colormaps.Div_precip()
r_cld=from_binary('r_calibration_cloud').r
srm_filename=os.path.join(constants.output_folder(),
                 'scenario.exp-930.geoeng.cld.artificial.iter20_50yrs')
CO2x2_filename=os.path.join(constants.scenario_2xCO2())
homogeneous_filename=os.path.join(constants.output_folder(),'scenario.exp-931.geoeng.sw.artificial.frominput_x0.98007_same_gmean_50yrs')
cloud_srm_filename=constants.get_art_forcing_filename(srm_filename,
                output_path= constants.cloud_folder()+'/cld.artificial.iteration')
control=from_binary(constants.control_def_file())[['tsurf','precip','sw']]
srm=from_binary(srm_filename)[['tsurf','precip','sw']]
CO2x2=from_binary(CO2x2_filename)[['tsurf','precip','sw']]
homogeneous=from_binary(homogeneous_filename)[['tsurf','precip','sw']]
cloud_srm=from_binary(cloud_srm_filename).cloud
cloud_CO2x2=from_binary(constants.cloud_def_file()).cloud
solar_homogeneous=from_binary(constants.get_art_forcing_filename(homogeneous_filename)).solar
