# LIBRARIES
from myfuncs import *

# Read scenario and base file
filename = r'/Users/dmar0022/university/phd/greb-official/output/scenario.exp-20.2xCO2_80yrs.ctl'
filename_base = r'/Users/dmar0022/university/phd/greb-official/output/control.default'

filename = input_(filename,1)
filename_base = input_(filename_base,2)

# Read artificial forcing (if any)
try: filename_art_forcing = constants.get_art_forcing_filename(filename)
except:
    try: filename_art_forcing = get_art_forcing_filename(filename,'cloud')
    except:
        try: filename_art_forcing = get_art_forcing_filename(filename,'solar')
        except: filename_art_forcing = None
if filename_art_forcing: filename_art_forcing=input_(filename_art_forcing,3)

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

# Creating figures output directories
os.makedirs(outdir_absolute,exist_ok=True)
os.makedirs(outdir_anom,exist_ok=True)

# # Converting bin file to netCDF
# print('Converting files to netCDF...')
# bin2netCDF(filename)
# bin2netCDF(filename_base)

# Importing the data
data = from_binary(filename)
data_base = from_binary(filename_base)

#  Plotting absolute countours
print('Plotting absolute contours...')
# annual mean
data.annual_mean().plotall(outpath=outdir_absolute)
# sesonal cycle
data.seasonal_cycle().plotall(outpath=outdir_absolute)

#  Plotting anomalies contours
print('Plotting anomalies contours...')
# annual mean
data.annual_mean().anomalies(data_base).plotall(outpath=outdir_anom)
# sesonal cycle
data.seasonal_cycle().anomalies(data_base).plotall(outpath=outdir_anom)

# Plot artificial_forcing
# if filename_art_forcing:
#     print('Plotting artificial cloud "'+name_art_cloud+'"...')
#     plot_clouds(filename_art_forcing,outdir_diff)
#     plot_clouds(filename_art_forcing)
# # Delete netCDF files

print('Done!!!\n')
