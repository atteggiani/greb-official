# LIBRARIES
from greb_climatevar import * # Import self defined classes and function
ignore_warnings()

# Reading file name
filename = r'~/university/phd/greb-official/input/isccp.cloud_cover.clim'
filename = read_input(filename)
name = os.path.split(filename)[1]
outfile = filename + '.nc'

# Setting figures output directory
outdir=os.path.join('/Users/dmar0022/university/phd/greb-official/figures','input.'+name)
os.makedirs(outdir,exist_ok=True)

print('\nFILE: '+ name)
# Converting bin file to netCDF
print('Converting file to netCDF...')
bin2netCDF(filename)

# Importing the data cube
data=[iris.util.squeeze(d) for d in iris.load(outfile)]

data=data[0]
n=0
plt.figure(figsize=(12,9))
plot_absolute.from_cube(data[n,:,:],cmap=cm.Greys_r,
cmaplev = np.arange(0,1+0.05,0.05),cbticks = np.arange(0,1+0.05,0.05)).plot(projection = None)
plt.figure(figsize=(12,9))


# # Delete netCDF file
print('Deleting netCDF file...')
os.remove(outfile)
print('Done!!!')
