# LIBRARIES
from greb_climatevar import * # Import self defined classes and function
ignore_warnings()

# Reading file name
filename = r'/Users/dmar0022/university/phd/greb-official/output/control.exp-20.2xCO2'
filename = read_input(filename)
name = os.path.split(filename)[1]
outfile = filename + '.nc'

# Setting figures output directory
outdir=os.path.join('/Users/dmar0022/university/phd/greb-official/figures',name)
os.makedirs(outdir,exist_ok=True)

print('\nFILE: '+ name)
# Converting bin file to netCDF
print('Converting file to netCDF...')
bin2netCDF(filename)

# Importing the data cube
data = iris.load(outfile)
# Parse data
data = parsevar(data)

#  Plotting scenario run output countours
print('Plotting contours...')
for var in data:
    # annual mean
    plt.figure()
    plot_absolute.from_cube(var).to_annual_mean().assign_var().plot(outpath=outdir)
    # sesonal cycle
    plt.figure()
    plot_absolute.from_cube(var).to_seasonal_cycle().assign_var().plot(outpath=outdir)
# # Delete netCDF file
print('Deleting netCDF file...')
os.remove(outfile)
print('Done!!!')
