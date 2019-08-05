# LIBRARIES
from greb_climatevar import * # Import self defined classes and function
ignore_warnings()

# Read scenario and base file
filename = r'/Users/dmar0022/university/phd/greb-official/output/scenario.exp-931.geoeng.sw.artificial.frominput-7.6_80yrs.ctl'
filename_base = r'/Users/dmar0022/university/phd/greb-official/output/control.default'
# filename_art_forcing = '/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.frominputX1.1'

filename = input_(filename,1)
filename_base = input_(filename_base,2)

# Read artificial forcing (if any)
try: filename_art_forcing = get_art_cloud_filename(filename)
except:
    try: filename_art_forcing = get_art_solar_filename(filename)
    except: filename_art_forcing = None
if filename_art_forcing: filename_art_forcing=input_(filename_art_forcing,3)

name = os.path.split(filename)[1]
print('\nSCENARIO_FILE: ' + name)
outfile = filename + '.nc'

name_base = os.path.split(filename_base)[1]
print('BASE_FILE: ' + name_base)
outfile_base = filename_base + '.nc'

if filename_art_forcing:
    name_art_forcing = os.path.split(filename_art_forcing)[1]
    print('ARTIFICIAL_FORCING: ' + name_art_forcing)

# Setting figures output directories
outdir=os.path.join('/Users/dmar0022/university/phd/greb-official/figures',name)
outdir_absolute=os.path.join(outdir,'absolute')
outdir_diff=os.path.join(outdir,'diff_'+name_base)
outdir_variation = os.path.join(outdir,'variat_'+name_base)

# Creating figures output directories
os.makedirs(outdir_absolute,exist_ok=True)
os.makedirs(outdir_diff,exist_ok=True)
# os.makedirs(outdir_variation,exist_ok=True)

# Converting bin file to netCDF
print('Converting files to netCDF...')
bin2netCDF(filename)
bin2netCDF(filename_base)

# Importing the data cube
data = parsevar(iris.load(outfile))
data_base = parsevar(iris.load(outfile_base))

#  Plotting scenario run absolute countours
print('Plotting scenario contours...')
for var in data:
    # annual mean
    plt.figure()
    plot_param.from_cube(var).to_annual_mean().assign_var().plot(outpath=outdir_absolute)
    # sesonal cycle
    plt.figure()
    plot_param.from_cube(var).to_seasonal_cycle().assign_var().plot(outpath=outdir_absolute)
#  Plotting anomalies contours
print('Plotting anomalies contours...')
for var in data:
    print('{}'.format(var.var_name))
    # annual mean
    plt.figure()
    plot_param.from_cube(var).to_annual_mean().to_anomalies(data_base).assign_var().plot(outpath=outdir_diff)
    # sesonal cycle
    plt.figure()
    plot_param.from_cube(var).to_seasonal_cycle().to_anomalies(data_base).assign_var().plot(outpath=outdir_diff)

# #  Plotting variation contours
# print('Plotting variation contours...')
# for var in data:
#     # annual mean
#     plt.figure()
#     plot_param.from_cube(var).to_annual_mean().to_variation(data_base).assign_var().plot(outpath=outdir_variation)
#     # sesonal cycle
#     plt.figure()
#     plot_param.from_cube(var).to_seasonal_cycle().to_variation(data_base).assign_var().plot(outpath=outdir_variation)
# Plot artificial clouds
# if filename_art_forcing:
#     print('Plotting artificial cloud "'+name_art_cloud+'"...')
#     plot_clouds(filename_art_forcing,outdir_diff)
#     plot_clouds(filename_art_forcing)
# # Delete netCDF files
print('Deleting netCDF files...')
os.remove(outfile)
os.remove(outfile_base)
print('Done!!!')
