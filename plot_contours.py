# LIBRARIES
from greb_climatevar import * # Import self defined classes and function
ignore_warnings()

# Reading file namelistry:
filename = r'/Users/dmar0022/university/phd/greb-official/output/scenario.exp-930.geoeng.cld_artificial'
filename_base = r'/Users/dmar0022/university/phd/greb-official/output/control.default'

filename = read_input(filename)
# filename_base = check_control(filename)[1] if check_control(filename)[0] else filename_base
filename_base = read_input(filename_base,2)

name = os.path.split(filename)[1]
outfile = filename + '.nc'
name_base = os.path.split(filename_base)[1]
outfile_base = filename_base + '.nc'

# Setting figures output directory
outdir=os.path.join('/Users/dmar0022/university/phd/greb-official/figures',name)
outdir_diff=os.path.join('/Users/dmar0022/university/phd/greb-official/figures',
                    'diff_'+name+'_'+name_base)
# outdir=os.path.join('/Users/dmar0022/university/phd/greb-official/figures',
#                     'contours_'+name+'_'+name_base)
os.makedirs(outdir,exist_ok=True)
os.makedirs(outdir_diff,exist_ok=True)

print('\nFILE: ' + name)
print('CONTROL_FILE: ' + name_base)
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

# [var.var_name for var in data]
# n=1
#
# grid = plt.GridSpec(6, 7, wspace=.5, hspace=1.2)
# g1=grid[:3,:3]
# g2=grid[3:,:3]
# g3=grid[:,3:]
# plt.subplot(g1,projection = ccrs.Robinson())
# plt.subplot(g2,projection = ccrs.Robinson())
# plt.subplot(g3,projection = ccrs.Robinson())
#
# plt.subplot(g1,projection = ccrs.Robinson())
# plot_absolute.from_cube(data[n]).to_annual_mean().assign_var().plot()
# plt.subplot(g2,projection = ccrs.Robinson())
# plot_absolute.from_cube(data[n]).to_annual_mean().assign_var().plot()
# plt.subplot(g3,projection = ccrs.Robinson())
# plot_absolute.from_cube(data[n]).to_annual_mean().assign_var().plot(outpath=outdir)

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
# # Delete netCDF files
print('Deleting netCDF files...')
os.remove(outfile)
os.remove(outfile_base)
print('Done!!!')
