# LIBRARIES
from greb_climatevar import * # Import self defined classes and function
ignore_warnings()

# Reading file namelistry:
filename = r'/Users/dmar0022/university/phd/greb-official/output/scenario.exp-20.2xCO2'
filename = read_input(filename)
filename_base = r'/Users/dmar0022/university/phd/greb-official/output/control.exp-20.2xCO2'
filename_base = read_input(filename_base,2)

name = os.path.split(filename)[1]
outfile = filename + '.nc'
name_base = os.path.split(filename_base)[1]
outfile_base = filename_base + '.nc'

# Setting figures output directory
outdir=os.path.join('/Users/dmar0022/university/phd/greb-official/figures',
                    'diff_'+name+'_'+name_base)
os.makedirs(outdir,exist_ok=True)

print('\nFILE: ' + name)
print('BASE_FILE: ' + name_base)
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

#  Plotting (scenario run - control run) output countours
print('Plotting difference contours...')
for var in data:
    # annual mean
    plt.figure()
    plot_difference.from_cube(var).to_annual_mean().to_difference(data_base).assign_var().plot(outpath=outdir)
    # sesonal cycle
    plt.figure()
    plot_difference.from_cube(var).to_seasonal_cycle().to_difference(data_base).assign_var().plot(outpath=outdir)
# # Delete netCDF files
print('Deleting netCDF files...')
os.remove(outfile)
os.remove(outfile_base)
print('Done!!!')
