# LIBRARIES
from greb_climatevar import * # Import self defined classes and function
ignore_warnings()

# Read scenario and base file
filename = r'/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.cld.artificial.frominputX1.1'
filename_base = r'/Users/dmar0022/university/phd/greb-official/output/control.default'
# filename_art_cloud = '/Users/dmar0022/university/phd/greb-official/artificial_clouds/cld.artificial.frominputX1.1'

filename = input_file(filename,1)
filename_base = input_file(filename_base,2)
# Read artificial cloud (if any)
filename_art_cloud=get_art_cloud_filename(filename)
if filename_art_cloud: filename_art_cloud=input_file(filename_art_cloud,3)

name = os.path.split(filename)[1]
print('\nSCENARIO_FILE: ' + name)
outfile = filename + '.nc'

name_base = os.path.split(filename_base)[1]
print('BASE_FILE: ' + name_base)
outfile_base = filename_base + '.nc'

if filename_art_cloud:
    name_art_cloud = os.path.split(filename_art_cloud)[1]
    print('ARTIFICIAL_CLOUD: ' + name_art_cloud)
# Setting figures output directory
outdir=os.path.join('/Users/dmar0022/university/phd/greb-official/figures',name)
outdir_diff=os.path.join('/Users/dmar0022/university/phd/greb-official/figures',
                    'diff_'+name+'_'+name_base)
# outdir=os.path.join('/Users/dmar0022/university/phd/greb-official/figures',
#                     'contours_'+name+'_'+name_base)
os.makedirs(outdir,exist_ok=True)
os.makedirs(outdir_diff,exist_ok=True)

# Converting bin file to netCDF
print('Converting files to netCDF...')
bin2netCDF(filename)
bin2netCDF(filename_base)

# Importing the data cube
data = iris.load(outfile)
data_base = iris.load(outfile_base)
# Parse data
data = parsevar(data)
data_base = parsevar(data_base)

#  Plotting scenario run output countours
print('Plotting scenario contours...')
for var in data:
    # annual mean
    plt.figure()
    plot_absolute.from_cube(var).to_annual_mean().assign_var().plot(outpath=outdir)
    # sesonal cycle
    plt.figure()
    plot_absolute.from_cube(var).to_seasonal_cycle().assign_var().plot(outpath=outdir)
#  Plotting (scenario run - control run) output countours
print('Plotting difference contours...')
for var in data:
    # annual mean
    plt.figure()
    plot_difference.from_cube(var).to_annual_mean().to_difference(data_base).assign_var().plot(outpath=outdir_diff)
    # sesonal cycle
    plt.figure()
    plot_difference.from_cube(var).to_seasonal_cycle().to_difference(data_base).assign_var().plot(outpath=outdir_diff)
# Plot artificial clouds
if filename_art_cloud:
    print('Plotting artificial cloud "'+name_art_cloud+'"...')
    plt.figure()
    plot_artificial_clouds(filename_art_cloud,outdir)
    plt.figure()
    plot_artificial_clouds(filename_art_cloud,outdir_diff)
    plt.figure()
    plot_artificial_clouds(filename_art_cloud)
# # Delete netCDF files
print('Deleting netCDF files...')
os.remove(outfile)
os.remove(outfile_base)
print('Done!!!')
