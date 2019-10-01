# LIBRARIES
from myfuncs import *
from matplotlib.ticker import AutoMinorLocator

# Read scenario and base file
filename = r'/Users/dmar0022/university/phd/greb-official/output/scenario.exp-20.2xCO2_80yrs.ctl'
filename_base = r'/Users/dmar0022/university/phd/greb-official/output/control.default'

filename = input_(filename,1)
filename_base = input_(filename_base,2)

# Read artificial forcing (if any)
try:
    filename_art_forcing = constants.get_art_forcing_filename(filename)
except:
    filename_art_forcing = None

name = os.path.split(filename)[1]
print('\nSCENARIO_FILE: ' + name)
# outfile = filename + '.nc'

name_base = os.path.split(filename_base)[1]
print('BASE_FILE: ' + name_base)
# outfile_base = filename_base + '.nc'

if filename_art_forcing:
    name_art_forcing = os.path.split(filename_art_forcing)[1]
    print('ARTIFICIAL_FORCING: ' + name_art_forcing)

# Setting figures output directories
outdir=os.path.join('/Users/dmar0022/university/phd/greb-official/figures',name)
outdir_absolute=os.path.join(outdir,'absolute')
outdir_anom=os.path.join(outdir,'diff_'+name_base)
outdir_global_mean=os.path.join(outdir,'global_mean')

# Creating figures output directories
os.makedirs(outdir_absolute,exist_ok=True)
os.makedirs(outdir_anom,exist_ok=True)
os.makedirs(outdir_global_mean,exist_ok=True)

# Importing the data
data = from_binary(filename)
data_base=None if name_base == 'control.default' else from_binary(filename_base)

# ============================================================================ #
#  Plotting absolute countours
print('Plotting absolute contours...')
# annual mean
data.annual_mean().plotall(outpath=outdir_absolute)
# sesonal cycle
data.seasonal_cycle().plotall(outpath=outdir_absolute)

# ============================================================================ #
#  Plotting anomalies contours
print('Plotting anomalies contours...')
# annual mean
data.annual_mean().anomalies(data_base).plotall(outpath=outdir_anom)
# sesonal cycle
data.seasonal_cycle().anomalies(data_base).plotall(outpath=outdir_anom)

# ============================================================================ #
# Plotting global_mean annual data
print('Plotting global mean...')
gm=data.group_by('year').global_mean().to_celsius()
ctl_gm=from_binary(filename_base).global_mean().annual_mean().assign_coords(time=0).to_celsius()
gm = Dataset(xr.concat([gm,ctl_gm],dim='time',positions=[list(np.arange(1,gm.dims['time']+1))+[0]]),attrs=gm.attrs)
# TSURF
plt.figure()
plt.plot(gm.tsurf,color='black',linewidth=2.5,label='global_mean')
plt.plot(gm.tsurf[0],marker='o',markerfacecolor='r',markeredgecolor='r',
         color='w',markersize=5,label='pre-industrial')
plt.title('Surface Temperature')
plt.xlabel('years')
plt.ylabel('tsurf (°C)')
plt.ylim((ctl_gm.tsurf-1,ctl_gm.tsurf+4))
plt.gca().yaxis.set_minor_locator(AutoMinorLocator())
plt.legend(loc='best')
plt.grid(which='both',linestyle='--')
plt.savefig(os.path.join(outdir_global_mean,'tsurf.png'), bbox_inches='tight',dpi=300)
plt.close()

# PRECIP
plt.figure()
plt.plot(gm.precip,color='black',linewidth=2.5,label='global_mean')
plt.plot(gm.precip[0],marker='o',markerfacecolor='r',markeredgecolor='r',
         color='w',markersize=5,label='pre-industrial')
plt.title('Precipitation')
plt.xlabel('years')
plt.ylabel('precip (mm/d)')
plt.ylim((ctl_gm.precip-0.1,ctl_gm.precip+0.6))
plt.gca().yaxis.set_minor_locator(AutoMinorLocator())
plt.legend(loc='best')
plt.grid(which='both',linestyle='--')
plt.savefig(os.path.join(outdir_global_mean,'precip.png'), bbox_inches='tight',dpi=300)
plt.close()

# ============================================================================ #
# # Plotting artificial forcing
# art_forcing=from_binary(filename_art_forcing)[next(iter(from_binary(filename_art_forcing)))]
# art_forcing.annual_mean().plot()
# plt.gca().grid()
# art_forcing.annual_mean().anomalies().plot()
#
# plt.gca().set_title('ciao')
# if filename_art_forcing:
#     print('Plotting artificial forcing...')

print('Done!!!\n')
